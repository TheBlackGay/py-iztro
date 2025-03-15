from py_iztro import Astro


def main():
    # 大限盘要先获取命盘，再获取大限盘
    # 获取命盘
    astro = Astro()
    result = astro.by_solar("2000-8-16", 2, "女")
    # 格式化输出
    print(result.model_dump_json(by_alias=True, indent=4))

    # 获取大限
    print("--------")
    result = result.horoscope("2025-01-01",0)
    # 格式化输出
    print(result.model_dump_json(by_alias=True, indent=4))


if __name__ == "__main__":
    main()
