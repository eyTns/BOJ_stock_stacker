import inspect
import os
import re
import sys
from contextlib import redirect_stdout


class MultiFile:  # write to multiple files at once
    def __init__(self, *files):
        self.files = files

    def write(self, data):
        for file in self.files:
            file.write(data)

    def flush(self):
        for file in self.files:
            file.flush()






"""
이 부분은 메모장으로 활용하세요

문제
두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.

입력
첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)

출력
첫째 줄에 A+B를 출력한다.

예제 입력 1 
1 2
예제 출력 1 
3
"""

def solve():
    a, b = map(int, input().split())
    print(a+b)













def parse_problem_number(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    match = re.search(r'\s(\d+)번', content)
    if match:
        return int(match.group(1))
    else:
        return "solution"
        # raise ValueError("Problem number not found.")

def parse_samples(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    if '예제 입력' in content:
        sample_input_flag = '예제 입력'
        sample_output_flag = '예제 출력'
        has_sample_num = True
    else:
        sample_input_flag = 'InputCopy'
        sample_output_flag = 'OutputCopy'
        has_sample_num = False
    samples = content.split(sample_input_flag)
    samples = [s.strip() for s in samples if s.strip()][1:]
    # print(samples)
    parsed_samples = []
    for sample in samples:
        parts = sample.split(sample_output_flag)
        # print(parts)
        if len(parts) == 2:
            if has_sample_num:
                input_part = parts[0].strip().split('\n', 1)
                output_part = parts[1].strip().split('\n', 1)
            else:
                input_part = parts[0].strip()
                output_part = parts[1].strip()
            if isinstance(input_part, list):
                output_lines = output_part[1].split('\n')
                output = []
                for line in output_lines:
                    if line.startswith('출처') or line.startswith('힌트') or line.startswith('노트') or line.startswith('알고리즘 분류') or line.startswith('Codeforces (c) Copyright'):
                        break
                    output.append(line)
                parsed_samples.append({
                    'input': input_part[1].strip(),
                    'output': '\n'.join(output).strip()
                })
            else:
                output_lines = output_part.split('\n')
                output = []
                for line in output_lines:
                    if line.startswith('Codeforces (c) Copyright') or line=="Note":
                        break
                    output.append(line)
                parsed_samples.append({
                    'input': input_part.strip(),
                    'output': '\n'.join(output).strip()
                })

    return parsed_samples

def grade_samples(samples):
    for i, sample in enumerate(samples):
        with open('sample_input.txt', 'w') as fin_w:
            fin_w.write(sample['input'])
        sys.stdin = open('sample_input.txt', 'r')

        with open('user_output.txt', 'w') as fout_w, redirect_stdout(
            MultiFile(fout_w, sys.stdout)):
            solve()

        with open('user_output.txt', 'r') as fout_r:
            user_output = fout_r.read().strip()
            expected_output = sample['output'].strip()
            if user_output == expected_output:
                print(f"***** Test Case {i+1}: Yes\n")
            else:
                print(f"***** Test Case {i+1}: No")
                print(f"Expected:\n{expected_output}\n")

def save_user_code(problem_number):
    solve_lines = inspect.getsource(solve).splitlines()
    solve_content = "\n".join([line[4:] for line in solve_lines[1:]])
    os.makedirs(os.path.join(os.getcwd(), 'Python', 'saved'), exist_ok=True)
    file_path = os.path.join(os.getcwd(), 'Python', 'saved', f'{problem_number}.py')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(solve_content)
    print(f"***** Solve function content saved to {file_path}")

def main():
    filename = 'Python/raw_page.txt'
    problem_number = parse_problem_number(filename)
    samples = parse_samples(filename)
    grade_samples(samples)
    save_user_code(problem_number)

if __name__ == "__main__":
    main()
