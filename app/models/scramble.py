import random

class Scramble:
    def __init__(self, type='3x3x3'):
        self.face_groups = {
            'U': ['U', 'D'], 'D': ['U', 'D'],
            'L': ['L', 'R'], 'R': ['L', 'R'],
            'F': ['F', 'B'], 'B': ['F', 'B']
        }
        self.face_list = ['U', 'D', 'L', 'R', 'F', 'B']
        self.type = type

    def get_angle(self):
        return random.choice(["", "2", "'"])

    def random_steps(self) -> str:
        steps = []
        last_face = None  # Lưu lại bước trước đó

        for _ in range(self.get_step_count()):
            while True:
                new_face = random.choice(self.face_list)
                # Đảm bảo không trùng nhóm với bước trước
                if last_face is None or new_face not in self.face_groups[last_face]:
                    last_face = new_face
                    break

            step = new_face + self.get_angle()
            steps.append(step)

        return ' '.join(steps)

    def get_step_count(self) -> int:
        return {"3x3x3": 20, "2x2x2": 10, "4x4x4": 30, "5x5x5": 35}.get(self.type, 10)
