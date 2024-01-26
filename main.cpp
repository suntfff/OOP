#include <iostream>
int main()
{
	setlocale(LC_ALL, "ru");
	class sphere {
		int r;
	public:
		sphere (int(r)) {
			if (r > 0) {
				this->r = r;
			}
			else {
				std::cout << "Значение должно быть больше нуля" << std::endl;
			}
		}
		double volume() {
			return (4 * acos(-1) * pow(this->r, 3))/3;
		}
		double square() {
			return 4 * acos(-1) * pow(this->r, 2);
		}

	};
	double r;
	std::cout << "Введите значение радиуса:"; std::cin >> r; std::cout << std::endl;
	sphere a(r);
	std::cout<<"ОбЪем:"<<a.volume() << std::endl <<"Площадь поверхности:"<< a.square();
}