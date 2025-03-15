from py_iztro import Astro


def main():
    # 获取命盘
    astro = Astro()
    result = astro.by_solar("2000-8-16", 2, "女")
    print(result.model_dump_json(by_alias=True, indent=4))

    # 获取大限
    print("--------")
    result = result.horoscope("2025-01-01",0).model_dump_json(by_alias=True, indent=4)
    print(result)


if __name__ == "__main__":
    main()
