import math
import random
from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional

from item import Item, Food, Gold, Water


RESOURCES = ("gold", "water", "food")

# Names of the Player attributes the trader reads and writes
PLAYER_STOCK_ATTR = {"gold": "currGold", "water": "currWater", "food": "currFood"}
PLAYER_MAX_ATTR = {"water": "maxWater", "food": "maxFood"}  # gold has no cap

# tolerance for comparing floating point trade values
EPSILON = 1e-9


@dataclass(frozen=True)
class Bundle:
    """An amount of gold, water, and food (one side of a trade)."""
    gold: int = 0
    water: int = 0
    food: int = 0

    def __post_init__(self):
        for resource in RESOURCES:
            amount = getattr(self, resource)
            if isinstance(amount, bool) or not isinstance(amount, int):
                raise TypeError(f"{resource} must be a whole number, got {amount!r}")
            if amount < 0:
                raise ValueError(f"{resource} cannot be negative, got {amount}")

    def amount(self, resource: str) -> int:
        """How much of one resource ('gold', 'water', or 'food') this holds."""
        return getattr(self, resource)

    def isEmpty(self) -> bool:
        return all(self.amount(r) == 0 for r in RESOURCES)

    def __str__(self):
        parts = [f"{self.amount(r)} {r}" for r in RESOURCES if self.amount(r) > 0]
        return " and ".join(parts) if parts else "nothing"


@dataclass(frozen=True)
class TradeOffer:
    """One proposed deal, from the player's point of view."""
    offered: Bundle     # what the player hands over
    requested: Bundle   # what the player receives

    def __str__(self):
        return f"you give {self.offered}, you get {self.requested}"


class TradeStatus(Enum):
    """The possible outcomes of presenting an offer to a trader."""
    ACCEPTED = "accepted"        # deal done, resources exchanged
    COUNTERED = "countered"      # trader proposes a different deal
    REJECTED = "rejected"        # trader is out of patience and ends the talks
    INVALID = "invalid"          # the offer itself is impossible; nothing changed
    UNAVAILABLE = "unavailable"  # trader isn't taking offers right now


@dataclass
class TradeResponse:
    """What the trader says back after an offer."""
    status: TradeStatus
    message: str
    offer: Optional[TradeOffer] = None  # the deal made (ACCEPTED) or proposed (COUNTERED)

    @property
    def accepted(self) -> bool:
        return self.status == TradeStatus.ACCEPTED

    @property
    def countered(self) -> bool:
        return self.status == TradeStatus.COUNTERED

    @property
    def rejected(self) -> bool:
        return self.status == TradeStatus.REJECTED

    def __str__(self):
        text = f'[{self.status.name}] "{self.message}"'
        return f"{text} -> {self.offer}" if self.offer else text


class TraderState(Enum):
    """The states from the Trader state diagram."""
    IDLE = "Idle in Square"
    EVALUATING = "Evaluating Offer"
    COUNTER_OFFERING = "Counter-Offering"
    TRADE_ACCEPTED = "Trade Accepted"
    MAD = "Mad / Reject Trade"


class Trader:
    """
    The standard trader. It has an unlimited supply of gold, water, and food
    and trades at fixed relative values (PRICES), but always wants to come out
    slightly ahead so the player can't exploit it.

    Subclasses change its personality by overriding small hooks:
        requiredMargin()     how much extra value it demands this round
        isInsulting()        whether an offer is so low it ends the talks at once
        counterStrategies()  how it builds counter-offers (and in what order)
    and by passing different patience / margin / cooldown values.
    """

    # Relative worth of one unit of each resource. Gold is the currency, so it
    # is worth a bit more than a unit of water or food.
    PRICES = {"gold": 3, "water": 2, "food": 2}

    # Shared game clock for every trader (see advanceTurn).
    currentTurn = 0

    GREETING = "Greetings, traveller! I've got goods to swap."
    ACCEPT_LINE = "Deal! A pleasure doing business."
    COUNTER_LINE = "Not quite. How about this instead?"
    REJECT_LINE = "No deal. I'm done haggling with you for now."
    BUSY_ACCEPTED_LINE = "We've already traded today. Come back tomorrow."
    BUSY_MAD_LINE = "I'm still annoyed with you. Come back later."

    def __init__(
        self,
        patienceLimit: int = 3,
        baseMargin: float = 0.15,
        minMargin: float = 0.0,
        cooldownTurns: int = 1,
        rng: Optional[random.Random] = None,
    ):
        """
        patienceLimit  how many counter-offers it makes before it loses patience
        baseMargin     extra value it wants on top of a fair swap (0.15 = 15%)
        minMargin      the lowest margin it will ever accept
        cooldownTurns  turns it refuses to talk after getting mad
        rng            random source (pass a seeded Random for repeatable games)
        """
        self.name = "Travelling Trader"  # same for every type: the player can't tell them apart
        self.traderType = type(self).__name__
        self.patienceLimit = patienceLimit
        self.baseMargin = baseMargin
        self.minMargin = minMargin
        self.cooldownTurns = cooldownTurns
        self.rng = rng if rng is not None else random.Random()

        # The wares on offer. Supply is unlimited, so every item is repeating.
        coin = Gold("Gold Coin", 1)
        coin.repeatBonus = True
        self.inventory: List[Item] = [
            coin,
            Water("Water Flask", self.PRICES["water"], 1, True),
            Food("Trail Rations", self.PRICES["food"], 1, True),
        ]

        self.counterCount = 0                            # counter-offers made so far
        self._state = TraderState.IDLE
        self._pendingOffer: Optional[TradeOffer] = None  # the counter-offer on the table
        self._negotiationTurn = 0                        # turn the negotiation is on
        self._readyTurn = 0                              # turn the trader is available again

    # ------------------------------------------------------------------ #
    # Game clock
    # ------------------------------------------------------------------ #
    @classmethod
    def advanceTurn(cls):
        """Move every trader forward one turn. Call once per game turn."""
        Trader.currentTurn += 1  # always on Trader so all subclasses share one clock

    @classmethod
    def resetClock(cls):
        """Reset the shared clock (use when starting a new game)."""
        Trader.currentTurn = 0

    # ------------------------------------------------------------------ #
    # State
    # ------------------------------------------------------------------ #
    @property
    def state(self) -> TraderState:
        """The trader's current state (cooldowns are applied automatically)."""
        self._refresh()
        return self._state

    def _refresh(self):
        """Return to Idle if a cooldown has ended or a negotiation went stale."""
        now = Trader.currentTurn
        if self._state in (TraderState.TRADE_ACCEPTED, TraderState.MAD):
            if now >= self._readyTurn:
                self._becomeIdle()
        elif self._state == TraderState.COUNTER_OFFERING:
            # A negotiation only lasts for the turn it started on.
            if now > self._negotiationTurn:
                self._becomeIdle()

    def _becomeIdle(self):
        self._state = TraderState.IDLE
        self.counterCount = 0
        self._pendingOffer = None

    # ------------------------------------------------------------------ #
    # Showing what the trader has
    # ------------------------------------------------------------------ #
    def describeItems(self) -> str:
        """Return a description of the trader's wares."""
        lines = [f'{self.name}: "{self.GREETING}"', "  Wares (unlimited supply):"]
        lines += [f"   - {item.name}" for item in self.inventory]
        lines.append("  Rough values: "
                     + ", ".join(f"1 {r} = {self.PRICES[r]}" for r in RESOURCES))
        lines.append("  Offer me what you'll give and what you want in return.")
        return "\n".join(lines)

    def showItems(self):
        """Print the trader's wares (the 'showItems' step in the diagrams)."""
        print(self.describeItems())

    # ------------------------------------------------------------------ #
    # Personality hooks (overridden by subclasses)
    # ------------------------------------------------------------------ #
    def requiredMargin(self) -> float:
        """Extra value (as a fraction) the trader wants for this evaluation."""
        return max(self.minMargin, self.baseMargin)

    def isInsulting(self, offer: TradeOffer) -> bool:
        """True if the offer is so low the trader ends the talks immediately."""
        return False

    def counterStrategies(self) -> List[Callable]:
        """The ways this trader tries to build a counter-offer, in order."""
        return [self._shrinkRequest, self._raiseOffer]

    # ------------------------------------------------------------------ #
    # Public entry points
    # ------------------------------------------------------------------ #
    def trade(self, player, offer: TradeOffer) -> TradeResponse:
        """
        Present an offer (or a counter-offer) to the trader. This is the method
        the Player/Brain should call; it checks everything and returns a
        TradeResponse describing what happened.
        """
        self._refresh()

        if self._state == TraderState.TRADE_ACCEPTED:
            return TradeResponse(TradeStatus.UNAVAILABLE, self.BUSY_ACCEPTED_LINE)
        if self._state == TraderState.MAD:
            return TradeResponse(TradeStatus.UNAVAILABLE, self.BUSY_MAD_LINE)

        problem = self._validate(player, offer)
        if problem:
            return TradeResponse(TradeStatus.INVALID, problem)

        if self._pendingOffer is not None and offer == self._pendingOffer:
            return self.acceptTrade(player, offer)

        return self.evaluateOffer(player, offer)

    def acceptCounterOffer(self, player) -> TradeResponse:
        """Accept the trader's most recent counter-offer."""
        self._refresh()
        if self._pendingOffer is None:
            return TradeResponse(TradeStatus.INVALID, "There is no counter-offer to accept.")
        return self.trade(player, self._pendingOffer)

    def walkAway(self):
        """The player ends a negotiation without a deal (no hard feelings)."""
        self._refresh()
        if self._state == TraderState.COUNTER_OFFERING:
            self._becomeIdle()

    # ------------------------------------------------------------------ #
    # Decision making (the Evaluating Offer state)
    # ------------------------------------------------------------------ #
    def evaluateOffer(self, player, offer: TradeOffer) -> TradeResponse:
        """
        Decide whether to accept, counter, or reject. Expects an offer that has
        already passed validation (trade() does this for you).
        """
        margin = self.requiredMargin()  # decided once so a whole evaluation is consistent
        self._state = TraderState.EVALUATING

        if self.checkOfferFairness(offer, margin):
            return self.acceptTrade(player, offer)

        # The offer is too low. Can the trader still be bothered to haggle?
        if self.isInsulting(offer) or not self.checkPatience():
            return self.rejectTrade()

        counter = self.makeCounterOffer(player, offer, margin)
        if counter is None:
            return self.rejectTrade()  # no workable deal exists
        return self.presentTrade(counter)

    def valueOf(self, bundle: Bundle) -> float:
        """The total trade value of a bundle."""
        return sum(self.PRICES[r] * bundle.amount(r) for r in RESOURCES)

    def checkOfferFairness(self, offer: TradeOffer, margin: Optional[float] = None) -> bool:
        """True if what the trader receives is worth enough for what it gives."""
        if margin is None:
            margin = self.requiredMargin()
        received = self.valueOf(offer.offered)
        given = self.valueOf(offer.requested)
        return received + EPSILON >= given * (1 + margin)

    def checkPatience(self) -> bool:
        """True if the trader will still make another counter-offer."""
        return self.counterCount < self.patienceLimit

    # ------------------------------------------------------------------ #
    # Actions (the outcomes in the state diagram)
    # ------------------------------------------------------------------ #
    def acceptTrade(self, player, offer: TradeOffer) -> TradeResponse:
        """Trade Accepted: swap the resources and rest until the next turn."""
        self.exchangeResources(player, offer)
        self._state = TraderState.TRADE_ACCEPTED
        self._readyTurn = Trader.currentTurn + 1
        self._pendingOffer = None
        return TradeResponse(TradeStatus.ACCEPTED, self.ACCEPT_LINE, offer)

    def presentTrade(self, counter: TradeOffer) -> TradeResponse:
        """Counter-Offering: put a new proposal on the table."""
        self.counterCount += 1
        self._state = TraderState.COUNTER_OFFERING
        self._pendingOffer = counter
        self._negotiationTurn = Trader.currentTurn
        return TradeResponse(TradeStatus.COUNTERED, self.COUNTER_LINE, counter)

    def rejectTrade(self) -> TradeResponse:
        """Mad / Reject Trade: end the talks and refuse to deal for a while."""
        self.endNegotiation()
        self._state = TraderState.MAD
        self._readyTurn = Trader.currentTurn + self.cooldownTurns
        return TradeResponse(TradeStatus.REJECTED, self.REJECT_LINE)

    def endNegotiation(self):
        """Throw away any counter-offer that was on the table."""
        self._pendingOffer = None

    def exchangeResources(self, player, offer: TradeOffer):
        """Move the resources: the player pays `offered` and receives `requested`."""
        problem = self._validate(player, offer)
        if problem:
            raise ValueError(problem)
        for resource in RESOURCES:
            attr = PLAYER_STOCK_ATTR[resource]
            newAmount = (getattr(player, attr, 0)
                         - offer.offered.amount(resource)
                         + offer.requested.amount(resource))
            cap = self._capacity(player, resource)
            if cap is not None:
                newAmount = min(newAmount, cap)  # current can never exceed max
            setattr(player, attr, newAmount)

    # ------------------------------------------------------------------ #
    # Building counter-offers
    # ------------------------------------------------------------------ #
    def makeCounterOffer(self, player, offer: TradeOffer, margin: float) -> Optional[TradeOffer]:
        """Try each strategy in turn; return the first fair, affordable counter."""
        for strategy in self.counterStrategies():
            counter = strategy(player, offer, margin)
            if (counter is not None
                    and counter != offer
                    and self._validate(player, counter) is None
                    and self.checkOfferFairness(counter, margin)):
                return counter
        return None

    def _shrinkRequest(self, player, offer: TradeOffer, margin: float) -> Optional[TradeOffer]:
        """Counter by giving less: keep the player's payment, cut what they get."""
        budget = self.valueOf(offer.offered) / (1 + margin)
        amounts = {r: offer.requested.amount(r) for r in RESOURCES}

        def total():
            return sum(self.PRICES[r] * amounts[r] for r in RESOURCES)

        while total() > budget + EPSILON:
            # Remove one unit from whichever resource is worth the most.
            biggest = max((r for r in RESOURCES if amounts[r] > 0),
                          key=lambda r: self.PRICES[r] * amounts[r])
            amounts[biggest] -= 1

        smaller = Bundle(**amounts)
        if smaller.isEmpty():
            return None  # the payment can't even buy one unit
        return TradeOffer(offer.offered, smaller)

    def _raiseOffer(self, player, offer: TradeOffer, margin: float) -> Optional[TradeOffer]:
        """Counter by asking for more: keep what they get, raise the payment."""
        needed = self.valueOf(offer.requested) * (1 + margin) - self.valueOf(offer.offered)
        amounts = {r: offer.offered.amount(r) for r in RESOURCES}

        # Ask for more of what they already offered first, then anything else
        # they have that isn't part of what they're requesting.
        order = ([r for r in RESOURCES if amounts[r] > 0]
                 + [r for r in RESOURCES
                    if amounts[r] == 0 and offer.requested.amount(r) == 0])

        for resource in order:
            if needed <= EPSILON:
                break
            spare = self._held(player, resource) - amounts[resource]
            if spare <= 0:
                continue
            units = min(spare, math.ceil((needed - EPSILON) / self.PRICES[resource]))
            amounts[resource] += units
            needed -= units * self.PRICES[resource]

        if needed > EPSILON:
            return None  # the player can't afford a fair price
        return TradeOffer(Bundle(**amounts), offer.requested)

    # ------------------------------------------------------------------ #
    # Checking that an offer is actually possible
    # ------------------------------------------------------------------ #
    @staticmethod
    def _held(player, resource: str) -> int:
        """Whole units of a resource the player currently has."""
        return int(math.floor(getattr(player, PLAYER_STOCK_ATTR[resource], 0)))

    @staticmethod
    def _capacity(player, resource: str) -> Optional[float]:
        """The most of a resource the player can carry, or None if uncapped."""
        attr = PLAYER_MAX_ATTR.get(resource)
        return getattr(player, attr, None) if attr else None

    def _validate(self, player, offer: TradeOffer) -> Optional[str]:
        """Return a reason the offer is impossible, or None if it is fine."""
        if offer.offered.isEmpty() or offer.requested.isEmpty():
            return "A trade needs something offered and something requested."

        for resource in RESOURCES:
            giving = offer.offered.amount(resource)
            getting = offer.requested.amount(resource)
            if giving and getting:
                return f"You can't offer and request {resource} in the same trade."

            have = self._held(player, resource)
            if giving > have:
                return f"You only have {have} {resource} but offered {giving}."

            cap = self._capacity(player, resource)
            if cap is not None and have + getting > cap:
                return f"You can't carry that much {resource} (maximum {cap})."
        return None

    def __repr__(self):
        return f"<{self.traderType} state={self.state.name} counters={self.counterCount}>"


class GrumpyTrader(Trader):
    """
    Short-tempered and greedy. Wants a big margin, only makes two counter-offers
    before losing his temper, sulks for several turns afterwards, and storms off
    immediately if an offer is insultingly low. His counter-offers demand that
    the player pay more rather than accept less.
    """
    GREETING = "What do you want? Make it quick."
    ACCEPT_LINE = "Hmph. Fine. Take it and go."
    COUNTER_LINE = "Is that the best you've got? Try this."
    REJECT_LINE = "Enough! Get out of my sight!"
    BUSY_ACCEPTED_LINE = "We're done for today. Leave me be."
    BUSY_MAD_LINE = "I said get lost!"

    INSULT_RATIO = 0.5  # offers worth under half of what is asked are insulting

    def __init__(self, rng: Optional[random.Random] = None):
        super().__init__(patienceLimit=2, baseMargin=0.30, cooldownTurns=3, rng=rng)

    def isInsulting(self, offer: TradeOffer) -> bool:
        return self.valueOf(offer.offered) < self.INSULT_RATIO * self.valueOf(offer.requested)

    def counterStrategies(self) -> List[Callable]:
        return [self._raiseOffer, self._shrinkRequest]


class FickleTrader(Trader):
    """
    Changes its mind. The margin it demands is re-rolled for every offer, so the
    same offer can be refused one moment and accepted the next. Once it has made
    a counter-offer, though, it sticks to it.
    """
    GREETING = "Ah, a customer! Let's see what mood I'm in today..."
    ACCEPT_LINE = "You know what? Yes! Deal!"
    COUNTER_LINE = "Hmm, on second thought, what about this?"
    REJECT_LINE = "I've changed my mind about the whole thing. Goodbye!"

    def __init__(self, rng: Optional[random.Random] = None):
        # baseMargin is the highest margin it might demand; minMargin the lowest.
        super().__init__(patienceLimit=4, baseMargin=0.45, minMargin=0.0, rng=rng)

    def requiredMargin(self) -> float:
        return self.rng.uniform(self.minMargin, self.baseMargin)


class FriendlyTrader(Trader):
    """
    Starts with a decent margin but warms up to the player: every counter-offer
    lowers the margin it demands. Very patient, but never gives goods away
    (it always keeps a small minimum profit).
    """
    GREETING = "Welcome, friend! Sit, rest, let's find a deal that suits us both."
    ACCEPT_LINE = "Wonderful! Safe travels, friend."
    COUNTER_LINE = "Close! Let's meet in the middle, shall we?"
    REJECT_LINE = "Sorry, friend, we just can't agree today."

    SOFTENING_PER_COUNTER = 0.05  # margin drops by this much per counter-offer

    def __init__(self, rng: Optional[random.Random] = None):
        super().__init__(patienceLimit=5, baseMargin=0.20, minMargin=0.05, rng=rng)

    def requiredMargin(self) -> float:
        softened = self.baseMargin - self.SOFTENING_PER_COUNTER * self.counterCount
        return max(self.minMargin, softened)


# Every kind of trader the game can place on the map
TRADER_TYPES = (Trader, GrumpyTrader, FickleTrader, FriendlyTrader)


def createRandomTrader(rng: Optional[random.Random] = None) -> Trader:
    """Create a trader of a randomly chosen type (the player can't tell which)."""
    chooser = rng if rng is not None else random
    return chooser.choice(TRADER_TYPES)()


class _DemoPlayer:
    """A minimal stand-in for the real Player, used only by the demo."""

    def __init__(self):
        self.currGold = 5
        self.currWater = 6
        self.currFood = 6
        self.maxWater = 20
        self.maxFood = 20

    def __str__(self):
        return (f"You have {self.currGold} gold, {self.currWater}/{self.maxWater} water, "
                f"{self.currFood}/{self.maxFood} food.")


def _parseBundle(text: str) -> Bundle:
    """Turn text like '2 food and 1 gold' into a Bundle."""
    tokens = [t for t in text.replace(",", " ").replace("+", " ").split() if t.lower() != "and"]
    if not tokens or len(tokens) % 2:
        raise ValueError("Write amounts like '2 food and 1 gold'.")
    amounts = {}
    for i in range(0, len(tokens), 2):
        try:
            count = int(tokens[i])
        except ValueError:
            raise ValueError(f"'{tokens[i]}' is not a whole number.")
        resource = tokens[i + 1].lower()
        if resource not in RESOURCES:
            raise ValueError(f"'{resource}' isn't tradeable. Use gold, water, or food.")
        amounts[resource] = amounts.get(resource, 0) + count
    return Bundle(**amounts)


def _parseOffer(text: str) -> TradeOffer:
    """Turn text like '2 food and 1 gold for 3 water' into a TradeOffer."""
    parts = text.lower().split(" for ")
    if len(parts) != 2:
        raise ValueError("Write an offer like: 2 food and 1 gold for 3 water")
    return TradeOffer(_parseBundle(parts[0]), _parseBundle(parts[1]))


def _playInteractively():
    """Let a person haggle with a trader of their choice."""
    print("Pick a trader:")
    for number, kind in enumerate(TRADER_TYPES, start=1):
        print(f"  {number}. {kind.__name__}")
    print(f"  {len(TRADER_TYPES) + 1}. Random")
    try:
        choice = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return
    if choice.isdigit() and 1 <= int(choice) <= len(TRADER_TYPES):
        trader = TRADER_TYPES[int(choice) - 1]()
    else:
        trader = createRandomTrader()

    player = _DemoPlayer()
    Trader.resetClock()
    print()
    trader.showItems()
    print("\nAt the > prompt, type one of:")
    print("  an offer, written as: <what you give> for <what you get>")
    print("      example:  3 gold and 2 food for 6 water")
    print("  accept   take the trader's last counter-offer")
    print("  next     let a day pass (traders trade once per day)")
    print("  quit     leave (exit and q also work)\n")

    while True:
        print(f"[turn {Trader.currentTurn}] {player}")
        try:
            command = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if command == "":
            continue
        if command in ("quit", "exit", "q"):
            break
        if command == "next":
            Trader.advanceTurn()
            print("A new day dawns.\n")
            continue
        if command in ("accept", "a"):
            response = trader.acceptCounterOffer(player)
        else:
            try:
                response = trader.trade(player, _parseOffer(command))
            except ValueError as error:
                print(f"  Sorry, I didn't understand that. {error}")
                print("  (Or type accept, next, or quit.)\n")
                continue
        print(f"  Trader: {response}\n")


def _runAutomatedDemo():
    """Show every trader type facing a haggler who accepts, and one who won't budge."""
    scenarios = (("accepts the first counter-offer", True),
                 ("never changes the offer", False))
    # trader's opening margin, so each personality has to decide how to react
    nearlyFair = TradeOffer(Bundle(gold=3, food=2), Bundle(water=6))
    for kind in TRADER_TYPES:
        for description, acceptsCounter in scenarios:
            Trader.resetClock()
            trader = kind(rng=random.Random(3))
            player = _DemoPlayer()
            print(f"=== {kind.__name__}: player {description} ===")
            print(f"  {player}")
            print(f"  Player offers: {nearlyFair}")
            for _ in range(10):
                response = trader.trade(player, nearlyFair)
                print(f"  Trader: {response}")
                if response.countered and acceptsCounter:
                    print("  Player accepts the counter-offer.")
                    response = trader.acceptCounterOffer(player)
                    print(f"  Trader: {response}")
                if not response.countered or acceptsCounter:
                    break
            print(f"  Result: {trader.state.value}. {player}\n")


if __name__ == "__main__":
    import sys
    if "--auto" in sys.argv:
        _runAutomatedDemo()
    else:
        _playInteractively()