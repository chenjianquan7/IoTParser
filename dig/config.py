import os

ROOT_PATH = os.path.split(os.path.abspath(__file__))[0]

HEADLESS_GHIDRA = os.path.join(ROOT_PATH, "ghidra", "support", "analyzeHeadless")

GHIDRA_SCRIPT = os.path.join(ROOT_PATH, "headless")
if __name__ == "__main__":
    print(ROOT_PATH)
    print(HEADLESS_GHIDRA)
    print(GHIDRA_SCRIPT)
