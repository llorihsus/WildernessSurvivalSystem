from vision import Vision
from path import Path

class Brain:
    def getPath(self, vision: Vision) -> Path:
        return Path()

    def makeMove(self, path: Path) -> bool:
        return True

    def stay(self) -> bool:
        return False

    def showAttributes(self, player) -> str:
        return ""