from logs.logs import logs
from copy import deepcopy


class GameHistoryTracer():
    def __init__(self, logs_string):
        self.logs_string = logs_string
        self.parsed_logs = []
        self.height = 0
        self.width = 0
        self.n = 0


    def update_game_fields(self, game_field_with_tracing, game_field_without_tracing, moves, valid_position, invalid_positions):
        parsed = list(map(int, moves.split()))
        game_field_with_tracing, game_field_without_tracing = self.update_valid_positions(game_field_with_tracing,
                                                                                          game_field_without_tracing,
                                                                                          valid_position)
        game_field_with_tracing, game_field_without_tracing = self.update_invalid_positions(game_field_with_tracing,
                                                                                            game_field_without_tracing,
                                                                                            invalid_positions)
        for i in [0, 2, 4, 6, 8]:
            game_field_with_tracing[parsed[i]][parsed[i+1]] = 'P' if i == 8 else 'E'
            game_field_without_tracing[parsed[i]][parsed[i+1]] = 'P' if i == 8 else 'E'


        return game_field_with_tracing, game_field_without_tracing


    def update_valid_positions(self, game_field_with_tracing, game_field_without_tracing, valid_positions):
        for x, y in valid_positions:
            game_field_with_tracing[x][y] = 'V'
            game_field_without_tracing[x][y] = 'V'
        return game_field_with_tracing, game_field_without_tracing


    def update_invalid_positions(self, game_field_with_tracing, game_field_without_tracing, invalid_positions):
        for x, y in invalid_positions:
            game_field_with_tracing[x][y] = 'I'
            game_field_without_tracing[x][y] = 'I'
        return game_field_with_tracing, game_field_without_tracing

    def parse_logs(self):
        game_field_with_tracing = game_field_without_tracing = None
        first_go = True
        debug_data = []
        round_input = ""
        output_data = ""
        output_stream = False
        invalid_positions = set()
        valid_positions = set()
        for line in self.logs_string.split('\n'):
            if 'Standard Error' in line and not first_go:
                game_field_without_tracing = [list('.'*self.width) for _ in range(self.height)]
                game_field_with_tracing, game_field_without_tracing = self.update_game_fields(game_field_with_tracing,
                                                                                              game_field_without_tracing,
                                                                                              moves,
                                                                                              valid_positions,
                                                                                              invalid_positions)
                self.parsed_logs.append(
                    {
                        'game_field_with_tracing': deepcopy(game_field_with_tracing),
                        'game_field_without_tracing': deepcopy(game_field_without_tracing),
                        'debug_data': debug_data,
                        'output_data': output_data,
                        'round_input': round_input
                    }
                )
                debug_data = []
                round_input = ""
                output_data = ""
                invalid_positions = set()
                valid_positions = set()
            elif 'Standard Error' in line and first_go:
                first_go = False
                continue
            elif 'invalid_positions' in line:
                invalid_positions = eval(line.split(':')[1])
            elif 'valid_position' in line:
                valid_positions = eval(line.split(':')[1])
            elif 'Console' in line:
                continue
            elif 'Init:' in line:
                splitted_line = line.split()
                self.width = int(splitted_line[1])
                self.height = int(splitted_line[2])
                if game_field_with_tracing is None:
                    game_field_with_tracing = [list('.'*self.width) for _ in range(self.height)]
            elif "Standard Output Stream:" in line:
                output_stream = True
            elif output_stream:
                output_data = line
                output_stream = False
            elif "moves: " in line:
                round_input = line[6:15]
                moves = line[16:]
            else:
                debug_data.append(line)
        game_field_without_tracing = [list('.'*self.width) for _ in range(self.height)]
        game_field_with_tracing, game_field_without_tracing = self.update_game_fields(game_field_with_tracing,
                                                                                      game_field_without_tracing,
                                                                                      moves,
                                                                                      valid_positions,
                                                                                      invalid_positions)

        self.parsed_logs.append(
            {
                'game_field_with_tracing': deepcopy(game_field_with_tracing),
                'game_field_without_tracing': deepcopy(game_field_without_tracing),
                'debug_data': debug_data,
                'output_data': output_data,
                'round_input': round_input
            }
        )
    
    def get_next(self):
        self.n += 1
        if self.n < len(self.parsed_logs):
            item = self.parsed_logs[self.n]
        else:
            # self.n = 0
            raise StopIteration
        return item


    def get_previous(self):
        self.n -= 1
        if self.n != -1:
            item = self.parsed_logs[self.n]
        else:
            # self.n = 0
            raise StopIteration
        return item


    def get_current(self):
        return self.parsed_logs[self.n]


    def reset_counter(self):
        self.n = 0



round_input = GameHistoryTracer(logs)
round_input.parse_logs()
