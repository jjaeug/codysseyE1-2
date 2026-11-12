import json
import os


DATA_FILE = "state.json"


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def get_default_data(self):
        return {
            "best_score": 0,
            "quizzes": [
                {
                    "question": "파이썬에서 출력할 때 사용하는 함수는?",
                    "choices": ["print", "input", "len", "type"],
                    "answer": 1
                },
                {
                    "question": "리스트를 만들 때 사용하는 괄호는?",
                    "choices": ["()", "{}", "[]", "<>"],
                    "answer": 3
                },
                {
                    "question": "조건문에 사용하는 키워드는?",
                    "choices": ["for", "if", "def", "class"],
                    "answer": 2
                },
                {
                    "question": "반복문 중 정해진 범위를 반복할 때 자주 쓰는 키워드는?",
                    "choices": ["for", "if", "try", "return"],
                    "answer": 1
                },
                {
                    "question": "파이썬에서 함수를 정의할 때 사용하는 키워드는?",
                    "choices": ["class", "def", "import", "while"],
                    "answer": 2
                }
            ]
        }

    def build_quiz(self, item):
        if not isinstance(item, dict):
            raise ValueError("퀴즈 항목이 객체가 아닙니다.")

        question = item["question"]
        choices = item["choices"]
        answer = item["answer"]

        if not isinstance(question, str) or question.strip() == "":
            raise ValueError("question이 비어 있거나 문자열이 아닙니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("choices는 4개여야 합니다.")

        for choice in choices:
            if not isinstance(choice, str) or choice.strip() == "":
                raise ValueError("choices에 비어 있거나 문자열이 아닌 값이 있습니다.")

        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("answer는 1~4 사이의 정수여야 합니다.")

        return Quiz(question, choices, answer)

    def parse_data(self, data):
        if not isinstance(data, dict):
            raise ValueError("최상위 데이터가 객체가 아닙니다.")

        best_score = data["best_score"]
        quiz_items = data["quizzes"]

        if isinstance(best_score, bool) or not isinstance(best_score, int) or best_score < 0:
            raise ValueError("best_score는 0 이상의 정수여야 합니다.")

        if not isinstance(quiz_items, list):
            raise ValueError("quizzes는 목록이어야 합니다.")

        quizzes = [self.build_quiz(item) for item in quiz_items]
        return best_score, quizzes

    def reset_to_default(self):
        self.best_score, self.quizzes = self.parse_data(self.get_default_data())
        self.save_data()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            print("데이터 파일이 없어 기본 퀴즈 데이터로 시작합니다.")
            self.reset_to_default()
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.best_score, self.quizzes = self.parse_data(data)

        except json.JSONDecodeError:
            print("JSON 파일 형식이 잘못되었습니다. 기본 데이터로 복구합니다.")
            self.reset_to_default()

        except (KeyError, TypeError, ValueError) as error:
            print(f"데이터 내용이 올바르지 않습니다({error!r}). 기본 데이터로 복구합니다.")
            self.reset_to_default()

        except OSError:
            print("데이터 파일을 읽을 수 없어 기본 퀴즈 데이터로 실행합니다.")
            self.best_score, self.quizzes = self.parse_data(self.get_default_data())

    def save_data(self):
        try:
            data = {
                "best_score": self.best_score,
                "quizzes": [
                    {
                        "question": quiz.question,
                        "choices": quiz.choices,
                        "answer": quiz.answer
                    }
                    for quiz in self.quizzes
                ]
            }

            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        except PermissionError:
            print("파일 저장 권한이 없습니다.")

        except OSError:
            print("파일 저장 중 시스템 오류가 발생했습니다.")

    def input_number(self, message, min_value, max_value):
        while True:
            try:
                value = input(message).strip()

                if value == "":
                    print("빈 입력은 사용할 수 없습니다.")
                    continue

                number = int(value)

                if number < min_value or number > max_value:
                    print(f"{min_value}부터 {max_value} 사이의 숫자를 입력하세요.")
                    continue

                return number

            except ValueError:
                print("숫자를 입력하세요.")

            except KeyboardInterrupt:
                print("\n입력이 중단되었습니다. 저장 후 종료합니다.")
                self.save_data()
                raise

            except EOFError:
                print("\n입력이 종료되었습니다. 저장 후 종료합니다.")
                self.save_data()
                raise

    def input_text(self, message):
        while True:
            value = input(message).strip()

            if value == "":
                print("빈 입력은 사용할 수 없습니다. 다시 입력하세요.")
                continue

            return value

    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n=== 퀴즈 풀기 ===")

        current_score = 0

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n문제 {index}.")
            quiz.display()

            user_answer = self.input_number("정답 번호 입력(1-4): ", 1, 4)

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                current_score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n결과: {len(self.quizzes)}문제 중 {current_score}문제 정답!")

        if current_score > self.best_score:
            self.best_score = current_score
            print("새로운 최고 점수입니다!")

        self.save_data()

    def show_score(self):
        if self.best_score == 0:
            print("\n아직 기록된 최고 점수가 없습니다.")
        else:
            print(f"\n최고 점수는 {self.best_score}점입니다.")

    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")

        question = self.input_text("문제를 입력하세요: ")

        choices = []

        for i in range(1, 5):
            choices.append(self.input_text(f"선택지 {i}: "))

        answer = self.input_number("정답 번호를 입력하세요(1-4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_data()

        print("새 퀴즈가 추가되었습니다.")

    def reset_score(self):
        print("\n=== 최고 점수 초기화 ===")

        confirm = input("정말 최고 점수를 초기화하시겠습니까? (y/n): ").strip().lower()

        if confirm == "y":
            self.best_score = 0
            self.save_data()
            print("최고 점수가 초기화되었습니다.")
        else:
            print("점수 초기화를 취소했습니다.")

    def show_quizzes(self):
        print("\n=== 퀴즈 목록 ===")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n{index}. {quiz.question}")
            for choice_index, choice in enumerate(quiz.choices, start=1):
                print(f"   {choice_index}. {choice}")
            print(f"   정답: {quiz.answer}번")

    def show_menu(self):
        while True:
            print("\n=== 콘솔 퀴즈 게임 ===")
            print("1. 퀴즈 풀기")
            print("2. 점수 보기")
            print("3. 퀴즈 추가")
            print("4. 점수 초기화")
            print("5. 퀴즈 목록 보기")
            print("6. 종료")

            choice = self.input_number("메뉴를 선택하세요: ", 1, 6)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.show_score()
            elif choice == 3:
                self.add_quiz()
            elif choice == 4:
                self.reset_score()
            elif choice == 5:
                self.show_quizzes()
            elif choice == 6:
                self.save_data()
                print("게임을 종료합니다.")
                break


def main():
    game = QuizGame()
    game.show_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n게임을 종료합니다.")
    except EOFError:
        print("\n입력이 종료되었습니다.")