



def reader():
    with open('symbols4.txt', 'r') as file:
        content = file.read()

    lines = content.split('\n')

    assets = []
    for line in lines:
        assets.append(line)

    return assets
 