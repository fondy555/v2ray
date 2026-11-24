import requests
import re


SOURCE_URLS = [
    "https://bestcf.pages.dev/gslege/Cfxyz.txt"
]



TEMPLATE = (
"vless://f344ee9c-0804-46bd-8c35-b2e2e89734c9@fondy.us.ci:443?encryption=none&security=tls&sni=fondy.us.ci&fp=chrome&alpn=http%2F1.1%2Ch3%2Ch2&type=xhttp&host=fondy.us.ci&path=%2F&mode=auto&extra=%7B%22mode%22%3A%22auto%22%2C%22xPaddingBytes%22%3A%22100-1000%22%7D#xhttp"

)


def get_ips():

    result = []
    seen = set()

    pattern = (
        r'(\d+\.\d+\.\d+\.\d+):(\d+)#地区随机\s*\|\s*([^\n]+)'
        r'|'
        r'(\d+\.\d+\.\d+\.\d+):(\d+)(#Gslege优选[^\n]*)'
    )

    for url in SOURCE_URLS:

        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            r.encoding = "utf-8"

        except requests.RequestException as e:
            print(f"获取失败: {url} -> {e}")
            continue

        for line in r.text.splitlines():

            m = re.search(pattern, line)

            if not m:
                continue

            if m.group(1):
                # 地区随机
                ip = m.group(1)
                port = m.group(2)
                country = m.group(3)

            else:
                # Gslege优选
                ip = m.group(4)
                port = m.group(5)
                country = m.group(6)

            addr = f"{ip}:{port}"

            if addr in seen:
                continue

            seen.add(addr)

            result.append((addr, country))

    return result



def build():

    nodes = ["vless://812803a8-b432-44cd-b33d-88e449acebcc@148.135.118.230:9527?encryption=mlkem768x25519plus.native.0rtt.sboUpcGvRIOrDsWcYygzLoA5DP0dqroI67x-5KFPx2U&security=none&type=httpupgrade&path=%2F#httpupgrade"]
    nodes.append(TEMPLATE)

    for addr,country in get_ips():

        node = TEMPLATE

        node = node.replace(
            "fondy.us.ci:443",
            addr
        )

        node = node.replace(
            "#xhttp",
            f"#{country}"
        )

        nodes.append(node)

    with open(
        "subscribe.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(nodes)
        )


if __name__ == "__main__":
    build()
