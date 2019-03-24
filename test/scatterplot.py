# Make sure we can include our source code from our test file.
import sys
sys.path.append('../bashplotlib')

from bashplotlib.scatterplot import build_scatter

if __name__ == "__main__":
    # Build a scatter plot
    scatter = build_scatter(
            [-10,20,30],
            [-10,20,30],
            10,
            'x',
            'default',
            'test hello')

    # This is what we know our scatter plot should
    # look like. We have to be careful that indentations
    # match.
    expected_scatter = """----------------------------
|        test hello        |
----------------------------
----------------------------
|                       x  |
|                          |
|                          |
|                   x      |
|                          |
|                          |
|                          |
|                          |
|                          |
|                          |
|                          |
| x                        |
----------------------------"""

    # Compare what we got to what we expected, and
    # fail with a helpful error message if anything is
    # different.
    if expected_scatter == scatter:
        print("SUCCESS!")
        sys.exit(0)
    else:
        print("FAILURE!")
        print("Expected:")
        print(expected_scatter)
        print("Got:")
        print(scatter)
        sys.exit(1)
