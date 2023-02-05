from dataclasses import asdict, dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    """Создать сообщение с информацией о тренировке"""
    def get_message(self):
        # Метод get_message() определяется в дочерних классах.
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance = self.get_distance()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = (self.action * self.LEN_STEP / self.M_IN_KM)
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed = (self.get_distance() / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(type(self).__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    COEF_CALORIES_1 = 18
    COEF_CALORIES_2 = 20

    def get_spent_calories(self) -> float:
        self.calories = ((self.COEF_CALORIES_1 * self.get_mean_speed()
                         - self.COEF_CALORIES_2) * self.weight
                         / Training.M_IN_KM * self.duration
                         * Training.M_IN_HOUR)
        return self.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CALORIES_1 = 0.035
    COEF_CALORIES_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    """Переопределена функция get_spent_calories()"""
    def get_spent_calories(self) -> float:
        self.calories = ((self.COEF_CALORIES_1 * self.weight
                         + (self.get_mean_speed() ** 2 // self.height)
                         * self.COEF_CALORIES_2 * self.weight)
                         * self.duration * Training.M_IN_HOUR)
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_CALORIES_1 = 1.1
    COEF_CALORIES_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool * self.count_pool
                      / Training.M_IN_KM / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        self.calories = ((self.get_mean_speed()
                         + self.COEF_CALORIES_1)
                         * self.COEF_CALORIES_2
                         * self.weight)
        return self.calories

    def get_distance(self) -> float:
        self.distance = (self.action * self.LEN_STEP / Training.M_IN_KM)
        return self.distance


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    training = workout_dict[workout_type](*data)
    if workout_type not in workout_dict:
        raise KeyError
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)