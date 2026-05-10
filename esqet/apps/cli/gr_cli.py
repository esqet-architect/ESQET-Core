import argparse
from esqet.gr.metric import minkowski

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--metric", default="minkowski")
    args = parser.parse_args()

    if args.metric == "minkowski":
        g = minkowski()

    print("Metric tensor:")
    print(g.g)
