class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 training_type: str = 'Running'
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = training_type

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        spent_calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * self.duration * self.M_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K1 = 0.035
    K2 = 0.029
    SM_IN_M = 100
    KMH_IN_MH = 0.278
    M_IN_HOUR = 60

    def __init__(self, action: int, duration: float, weight: float,
                 height: float, training_type: str = 'SportsWalking'):
        super().__init__(action, duration, weight)
        self.height = height
        self.training_type = training_type

    def get_spent_calories(self):
        spent_calories = (
            (self.K1 * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MH)**2
                    / (self.height / self.SM_IN_M)) * self.K2 * self.weight)
            * self.duration * self.M_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    K_3 = 1.1
    K_4 = 2
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: int,
                 count_pool: int, training_type: str = 'Swimming'
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.training_type = training_type

    def get_mean_speed(self):
        M_IN_KM = 1000
        mean_speed = (self.length_pool
                      * self.count_pool / M_IN_KM) / self.duration
        return mean_speed

    def get_spent_calories(self):
        spent_calories = (self.get_mean_speed()
                          + self.K_3) * self.K_4 * self.weight * self.duration
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == 'RUN':
        return Running(*data)
    elif workout_type == 'WLK':
        return SportsWalking(*data)


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
