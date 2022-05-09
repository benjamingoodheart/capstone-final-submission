
import subprocess
import time
from tqdm import tqdm

def run_cov_tests(i):
    test = subprocess.run(['coverage', 'run', 'manage.py', 'test'], capture_output=True, text=True)

    with open('test-results.txt', 'a') as file:
        print("-----------------------\n")
        print("\n |-\tTest #" + str(i+1) + "\t\t-| \n")
        print("-----------------------\n\n")
        file.write("-----------------------\n")
        file.write("\n |-\tTest #" + str(i+1) + "\t\t-| \n")
        file.write("-----------------------\n")
        file.write(test.stderr)
        file.write("\n")


if __name__ == "__main__":

    reps = input("Enter how many times we should test it : \n")
    title = input("Enter a title for this test set: ")
    with open('test-results.txt', 'a') as file:
        file.write("\n----------------\n")
        file.write("*******TEST NAME: " + str(title))
        
    reps = int(reps)

    start_time = time.time()
        
    for i in tqdm(range(reps), desc="Loading"): 
            try:
                    run_cov_tests(i)
            except:
                file.write("xxxxxxxxxxxxxx-FAILED-xxxxxxxxxxxxx")
                pass
    
    end_time = time.time()
    run_time = end_time - start_time
    with open('test-results.txt', 'a') as file:
        file.write("Ran in " + str(run_time) + " seconds")
    
    
