import os
import webbrowser
import shutil
from math import log
from textwrap import wrap

print()
metals = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Ruby']
metals_lower = [m.lower() for m in metals]
def padprint(k, v):
    print(f"{k}".rjust(15),f": {v}")





# 마라톤 푼 문제들의 티어로부터 퍼포먼스 출력
solved = "g5g3"

d = {"b":0, "s":5, "g":10, "p":15, "d":20, "r":25}
tier_list = [d[t[0]] + 6-int(t[1]) for t in wrap(solved, 2)]
performance = log(sum([2.4**i for i in tier_list]), 2.4)
padprint("Performance", f"{performance:.6f}")
print()




# 푼 문제 자동으로 옮기기
num_class_list = [
    "1000 b5",
    "99999 r1",
    "99998 un",
]

diff_dict = {m[0].lower(): m for m in metals}
source_dir_rel = "Python/saved"
for num_class in num_class_list:
    num, cd = num_class.split()
    file_name = f"{num}.py"
    if cd == "un":
        target_dir_rel = "Python/solved/Unrated"
        category = "Unrated"
    else:
        category = diff_dict[cd[0]]
        difficulty = cd[1:]
        target_dir_rel = f"Python/solved/{category}/{category} {difficulty}"
    target_path_rel = f"{target_dir_rel}/{file_name}"
    source_dir = os.path.join(os.getcwd(), source_dir_rel)
    target_dir = os.path.join(os.getcwd(), target_dir_rel)
    target_path = os.path.join(os.getcwd(), target_dir_rel, file_name)

    source_path = None
    for root, dirs, files in os.walk(source_dir):
        if file_name in files:
            source_path = os.path.join(root, file_name)
            break
    if source_path is None:
        padprint("File Mover", f"{file_name} not exist in {source_dir_rel}")
    else:
        os.makedirs(target_dir, exist_ok=True)
        shutil.move(source_path, target_path)
        padprint("File Mover", f"{file_name} moved to {target_dir_rel}")
print()





# 티어별 미리 풀어둔 문제 수 확인
def get_tier_info(file_path):
    parent_dir = os.path.basename(os.path.dirname(file_path))
    parts = parent_dir.split('_')
    if len(parts) == 2 and parts[0] in metals_lower:
        return parts[0], int(parts[1])
    return None, None

tier_counts = {metal: [0] * 5 for metal in metals_lower}

for root, dirs, files in os.walk(f"{os.getcwd()}/Python/saved"):
    for file in files:
        if file.endswith('.py') or file.endswith('.txt'):
            file_path = os.path.join(root, file)
            metal, number = get_tier_info(file_path)
            if metal and number:
                tier_counts[metal][number-1] += 1

cumul = 0
cumul_counts = []
for m in reversed(metals_lower):
    cumul += sum(tier_counts[m])
    cumul_counts.append(cumul)
cumul_counts.reverse()
cumul_counts = {k:v for (k, v) in zip(metals_lower, cumul_counts)}

ranked = 0
for metal in metals_lower:
    each_tier_string = ", ".join(str(x).rjust(2) for x in reversed(tier_counts[metal]))
    metal_tier_string = str(sum(tier_counts[metal])).rjust(3)
    cumul_string = str(cumul_counts[metal]).rjust(3)
    metal_string = " | ".join([each_tier_string, metal_tier_string, cumul_string])
    padprint(metal.capitalize(), metal_string)
    ranked += sum(tier_counts[metal])

cpt = sum([len(files) for r, d, files in os.walk(f"{os.getcwd()}/Python/saved")])
padprint("unclassified", cpt-ranked)
padprint("Saved problems", cpt)
print()





# 미리 풀어둔 문제 중에서 찾기
problem_list_to_find = """
27330
27331
27332
""".strip().split("\n")
saved_problem_dict = dict.fromkeys(problem_list_to_find)
for root, dirs, files in os.walk("Python/saved"):
    for file in files:
        problem_number = file.split(".")[0]
        tier = root.split("\\")[-1]
        if problem_number in saved_problem_dict:
            saved_problem_dict[problem_number] = tier
found = False
for problem in problem_list_to_find:
    if saved_problem_dict[problem]:
        found = True
        padprint("Find Problem", f"{problem:5} {saved_problem_dict[problem]:8} is already saved")
if found:
    print()





# 폴더에 있는 문제 제출하는 웹페이지 자동으로 열기
files = os.listdir("Python/saved/submit_this")
if files:
    url = "https://solved.ac"
    webbrowser.open(url)
for file in files:
    if file.lower().endswith('.py') or file.lower().endswith('.txt'):
        problem_number = file.split('.')[0]
        if problem_number.isdigit():
            url = f"https://www.acmicpc.net/problem/{problem_number}"
            webbrowser.open(url)
