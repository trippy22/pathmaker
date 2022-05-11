import requests
import uuid

def generate_path(start_x, start_y, end_x, end_y):
    headers = {
        "key": "sub_DPjXXzL5DeSiPf",
        "secret": "PUBLIC-KEY"
    }
    path = {
        "start": {
            "x": start_x,
            "y": start_y,
            "z": 0
        },
        "end": {
            "x": end_x,
            "y": end_y,
            "z": 0
        }
    }
    result = requests.post("https://api.dax.cloud/walker/generatePath", json=path, headers=headers).json()
    return result, result['pathStatus']


def format_path(data):
    msg = '''Position[] path = {\n'''
    for x, y in enumerate(data):
        if x == len(data) - 1:
            msg += f'''    new Position({y["x"]}, {y["y"]}, 0)\n'''
        else:
            msg += f'''    new Position({y["x"]}, {y["y"]}, 0),\n'''
    msg += '};'
    return msg


def main():
    data = []
    start_x, start_y, end_x, end_y = None, None, None, None
    while True:
        start_x = input('Enter start x: ').strip() if not start_x else end_x
        start_y = input('Enter start y: ').strip() if not start_y else end_y
        print(f'StartX/Y: {start_x} {start_y}')

        end_x = input('Enter end x: ').strip()
        end_y = input('Enter end y: ').strip()
        print(f'EndX/Y: {end_x} {end_y}')

        result, reason = generate_path(start_x, start_y, end_x, end_y)
        path = result['path']

        if path:
            data += path
            cont = input('Enter "stop" to save, or just press enter to keep adding more points: ')
            if cont == 'stop':
                break
        else:
            print(f'Invalid start/end points, reason: {reason}. Starting over')
            start_x = None
            end_x = None
            start_y = None
            end_y = None

    text = format_path(data)
    naming = str(uuid.uuid4())[0:3]
    with open(f'path-{naming}.txt', 'w') as f:
        f.write(text)


if __name__ == '__main__':
    main()
