from typing import List, Dict, Tuple, Union, Set
import sys
import json

class DfaSimulator:
    def __init__(
            self,
            states: Set[str],
            alphabet_list: Set[str],
            transition_func: Dict[Tuple[str, str], str],
            start_state: str,
            accept_states: List[str],
            test_cases: List[str]
        ):

        # 状態
        self.states: List[str] = states

        # アルファベット
        self.alphabet_list: List[str] = alphabet_list

        # 状態遷移関数 (状態, 入力) -> 遷移先状態
        self.transition_function: Dict[Tuple[str, str], str] = transition_func

        # 開始状態
        self.start_state: str = start_state

        #受理状態
        self.accept_states: List[str] = accept_states

        self.test_cases: List[str] = test_cases

    def execute(self) -> bool:
        for case in self.test_cases:
            current_state: str = self.start_state

            for char in case:
                state: Tuple[str, int] = (current_state, char)

                if (state in self.transition_function):
                    current_state = self.transition_function[state]
                else:
                    print('error')
                    print('満たされないケースが見つかりました!!')
                    print(f"case, {case}")
                    break

            if (current_state in self.accept_states):
                print(f"case: {case} は受理されました")
            else:
                print(f"case: {case} は受理されませんでした")


class ConfigFileLoader:
    def __init__(self, file_path):
        self.file = file_path

    def load_config(self) -> Union[Dict[str, Union[Set[str], Dict[Tuple[str, str], str], str, List[str]]], bool]:
        with open(self.file, 'r') as file:
            config = json.load(file)

        states = set(config["states"])
        alphabet_list = set(config["alphabet_list"])
        accept_states = set(config["accept_states"])
        transition_function = {tuple(key.split(',')): value for key, value in config["transition_function"].items()}
        start_state = config["start_state"]
        test_cases = config["test_cases"]

        if not self.validate_config(states, accept_states, transition_function, start_state, test_cases):
            return {}, False

        return {
            'states': states,
            'alphabet_list': alphabet_list,
            'transition_function': transition_function,
            'start_state': start_state,
            'accept_states': accept_states,
            'test_cases': test_cases,
        }, True

    def validate_config(
            self,
            states: Set[str],
            accept_states: Set[str],
            transition_function: Dict[Tuple[str, str], str],
            start_state: str,
            test_cases: List[str]
        ) -> bool:

        if not all(state in states for state in accept_states):
            print("Error: 一部の受入状態が状態セット内にありません")
            return False

        if not start_state in states:
            print("Error: 開始状態が状態セット内にありません")
            return False

        for (from_state, input_char), to_state in transition_function.items():
            if from_state not in states or to_state not in states:
                print("Error: 遷移関数に状態セットに含まれない状態が含まれています")
                return False

        return True

# コマンドライン引数を取得する
args = sys.argv[1:]  # 最初の要素はスクリプトのファイル名なので除外

loader = ConfigFileLoader(args[0])

result, is_valid = loader.load_config()

if (is_valid):
    simulator = DfaSimulator(
            result['states'],
            result['alphabet_list'],
            result['transition_function'],
            result['start_state'],
            result['accept_states'],
            result['test_cases'])
    simulator.execute()
else:
    print('DFA設定ファイルに誤りがあります。')
