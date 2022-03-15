from collections import Counter
import math
from re import L
from ortools.linear_solver import pywraplp
import numpy as np

def euclidean_distance(x , y):
    return math.sqrt(sum((a-b)**2 for (a ,b) in zip(x ,y)))

def data_matrix(p1 , p2):
    data_ = []
    for x in p1:
        x_list = []
        for y in p2:
            x_list.append(euclidean_distance(x , y))
        data_.append(x_list)
    return data_



def getAssignment(p1 , p2):
    assert(len(p1) == len(p2)) , "p1 and p2 must have same number of points"
    num_points = len(p1)
    data_ = data_matrix(p1 , p2)
    solver= pywraplp.Solver.CreateSolver("SCIP")

    # Creatinng the optimization variables
    x = {}
    for i in range(num_points):
        for j in range(num_points):
            x[i , j] = solver.IntVar(0 , 1 , '')
    
    # Adding the bijective Constraints
    for i in range(num_points):
        solver.Add(solver.Sum([x[i,j] for j in range(num_points)]) == 1)
    
    for j in range(num_points):
        solver.Add(solver.Sum([x[i,j] for i in range(num_points)]) == 1)
    
    # Objective function 
    objective_terms =[]
    for i in range(num_points):
        for j in range(num_points):
            objective_terms.append(data_[i][j] * x[i , j])
    solver.Minimize(solver.Sum(objective_terms))

    status = solver.Solve()
    ans_dict = {}
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("Bijection success")
        print("EMD (minimum work) = " , solver.Objective().Value()/num_points , "\n")
        for i in range(num_points):
            for j in range(num_points):
                if x[i , j].solution_value() > 0.5:
                    print(p1[i] , " assigned to " , p2[j])
                    ans_dict[i] = j
        return ans_dict
    else:
        print('No solution found.')



def interpolation(p1 , p2 , lmbda , ans_dict):
    assert 0 <= lmbda <= 1 , "lambda out of bounds"
    n = len(p1)
    for i in range(n):
        j = ans_dict[i]
        point1 = p1[i]
        point2 = p2[j]
        point1 = np.asarray(point1)
        point2 = np.asarray(point2)
        intermediate_point = (1 - lmbda) * point1 + lmbda * point2
        print("\n")
        print("Point1 is:" , point1)
        print("Point2 is:" , point2)
        print("Interpolated point : " , intermediate_point)
        print("-" * 20)

def get_interpolation(p1 , p2 , lmbda):
    print("Starting.....\n")
    ans_dict = getAssignment(p1 , p2)
    if ans_dict:
        interpolation(p1 , p2 , lmbda ,ans_dict)
    else:
        print("Interpolation not possible")

if __name__=="__main__":
    
    #Point set 1
    p1 = [
        (0, 0),
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
    ]

    #Point set 2
    p2 = [
        (0, 0),
        (0, 2),
        (0, -2),
        (2, 0),
        (-2, 0),
    ]
    get_interpolation(p1 , p2 , 0.6)
