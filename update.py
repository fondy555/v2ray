import requests
import re


SOURCE_URL = "https://ips.gaoji.uk/best_ips.txt"


TEMPLATE = (
    "vless://f344ee9c-0804-46bd-8c35-b2e2e89734c9@fondy.space:443?"
    "type=xhttp&encryption=none&path=%2F&host=fondy.space&mode=auto&"
    "x_padding_bytes=100-1000&extra=%7B%22mode%22%3A%22auto%22%2C%22xPaddingBytes%22%3A%22100-1000%22%7D&"
    "security=tls&fp=chrome&alpn=http%2F1.1%2Ch3%2Ch2&sni=fondy.space"
    "#优选IP-BR"
)


def get_ips():

    r = requests.get(
        SOURCE_URL,
        timeout=20
    )

    r.encoding = "utf-8"

    result = []
    seen = set()


    for line in r.text.splitlines():

        m = re.search(
            r"(\d+\.\d+\.\d+\.\d+):(\d+)#([A-Z]{2})",
            line
        )

        if not m:
            continue


        ip = m.group(1)
        port = m.group(2)
        country = m.group(3)


        addr = f"{ip}:{port}"


        if addr in seen:
            continue


        seen.add(addr)

        result.append(
            (
                addr,
                country
            )
        )

    return result



def build():

    nodes = []

    for addr,country in get_ips():

        node = TEMPLATE

        node = node.replace(
            "fondy.space:443",
            addr
        )

        node = node.replace(
            "#优选IP-BR",
            f"#优选IP-{country}"
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