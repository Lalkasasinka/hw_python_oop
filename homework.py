class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: int) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


LEN_STEP: float = 0.65
M_IN_KM: int = 1000


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    KMH_IN_MSEC: float = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        self.info = (InfoMessage(self.__class__.__name__,
                                 self.duration,
                                 self.get_distance(),
                                 self.get_mean_speed(),
                                 self.get_spent_calories()))
        return self.info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        caloires_formula = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                             * self.get_mean_speed()
                             + self.CALORIES_MEAN_SPEED_SHIFT)
                            * self.weight / self.M_IN_KM
                            * (self.duration * self.MIN_IN_H))
        return caloires_formula


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    KMH_IN_MSEC: int = 0.278
    POW_COEF: int = 2
    CM_IN_M: int = 100
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                     + ((self.get_mean_speed() * self.KMH_IN_MSEC)
                        ** self.POW_COEF / (self.height / self.CM_IN_M))
                     * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                    * (self.duration * self.MIN_IN_H))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SPEED_SHIFT: float = 1.1
    M_IN_KM: int = 1000
    CALLORIES_WEIGHT_MULTIPLIER: int = 2

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
                      / M_IN_KM / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        calories_formula = ((self.get_mean_speed() + 1.1)
                            * 2 * self.weight * self.duration)
        return calories_formula


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TRAINIG_CODE: dict[str, Training: str] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in TRAINIG_CODE:
        print('Такой тренировки нет')
    return TRAINIG_CODE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    Info = training.show_training_info()
    print(Info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
