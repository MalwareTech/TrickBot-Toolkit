from ConfigDecrypter import ConfigDecrypter
from includes import BotConfig
from includes import C2Communications
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help="file to download from C2", required=True)
    parser.add_argument('-o', '--output', help="output file")
    args = parser.parse_args()

    bot = BotConfig.Bot()

    servers = bot.get_servers()

    for server in servers:
        command = C2Communications.C2(bot, server)

        print('trying server: {}'.format(server))

        if not bot.config['registered']:
            response = command.register()
            result_code, data = response

            if result_code != 200:
                continue

            bot.config['registered'] = True

        if args.file == 'main':
            response = command.get_main_config()
        else:
            response = command.get_file(args.file)

        result_code, data = response

        if result_code == 404:
            print('Error: file does not exist')
            exit(0)

        if result_code == 403:
            bot.config['registered'] = False
            continue

        elif result_code != 200:
            continue

        decrypter = ConfigDecrypter(data)
        file_data = decrypter.decrypt()

        if args.output:
            output_file = open(args.output, 'w')
            output_file.write(file_data)
            output_file.close()
            print('saved output to {}'.format(args.output))
        else:
            print(file_data)

        bot.save_config()

        exit(0)

    raise RuntimeError("Failed to find a working C2, try finding a new list.")

