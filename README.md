# A* vs Best First  
This project is used to compare the performance of  A* and Best First search using different heuristics on 8 puzzles. This project was completed for an artificial intelligence course at my university.
# Testing method:
I used 3 different heuristics to search for a solution for different 8puzzles. Each heuristic was run with 5 different 8puzzle starting configurations. The A* search is using the function f(n) = g(n) + h(n). G(n) corresponds to the number of steps to get to the current puzzle state and h(n) is the evaluation of whatever heuristic is currently being used. The best first algorithm uses the function f(n) = h(n).
![image](https://user-images.githubusercontent.com/47011094/156479094-3258261c-a52d-460f-972e-f2482cccb093.png)
The puzzles are inputted as 2d arrays where [[0, 1, 2], [3, 4,5], [6, 7, 8]] would correspond to the image above. The puzzles that I chose to test with are as follows:
Puzzle 1:  [[1, 0, 3], [5, 2, 6], [4, 7, 8]]
Puzzle 2:  [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
Puzzle 3:  [[5, 1, 3], [2, 6, 0], [4, 7, 8]]
Puzzle 4:  [[0, 1, 5], [7, 4, 2], [8, 6, 3]]
Puzzle 5:  [[0, 1, 2], [5, 6, 3], [4, 7, 8]]

# Conclusions:
Averages steps between the 5 puzzles:
	A*:
		Heuristic 1: 109.2
		Heuristic 2: 470.8
		Heuristic 3: 116
		Average A*: 232


	Best-first:
		Heuristic 1: 109.6
		Heuristic 2: 470.8
		Heuristic 3: 116
		Average best-first: 232.13
 
 In conclusion, it seems that A* performs better than best-first when averaging the 3 heuristics together (232 steps vs 232.13).
