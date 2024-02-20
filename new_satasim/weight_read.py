import math

def print_status_bar(percentage):
    total_length = 20  # Total length of the progress bar
    filled_length = int(total_length * percentage // 100)  # Number of '=' to print
    bar = '[' + '=' * filled_length + ' ' * (total_length - filled_length) + ']'
    print(f'Line Occupied: {bar}  {percentage}%', end='')

def line_recorder(input_weights):
      line_words_n = 64
      word_bits_n  = 8
      weight_bits = 4

      left_weights = 0

      if weight_bits < word_bits_n:
        weights_per_word = math.floor(word_bits_n/weight_bits)
        row_capacity = line_words_n*weights_per_word
        if input_weights > row_capacity:
          total_weights = row_capacity
          left_weights = input_weights - total_weights
        else:
          total_weights = input_weights
          left_weights = 0
        actual_occupied = math.ceil(total_weights/weights_per_word)
        print(f'The weights are packed in one word, each word contains {weights_per_word} weights.')
      else:
        words_per_weight = math.ceil(weight_bits/word_bits_n)
        row_capacity = math.floor(line_words_n/words_per_weight)
        if input_weights > row_capacity:
          total_weights = row_capacity
          left_weights = input_weights - total_weights
        else:
          total_weights = input_weights
          left_weights = 0
        actual_occupied = words_per_weight*total_weights
        print(f'The weights are stored in multiple words, each weight requires {words_per_weight} words.')

      print(f'Each row can contain {row_capacity} weights.')
      print(f'Actual occupied {actual_occupied} words by {total_weights} weights')
      occ_percent = (actual_occupied/line_words_n)*100
      print_status_bar(occ_percent)

      return left_weights



def memory_filler(weight_counts):
  print(f"\nStart filling the memory. Total {weight_counts} weights to fill.")
  row = 0
  while weight_counts != 0:
    print(f"\n--- Row {row} ---")
    weight_counts = line_recorder(weight_counts)
    row+=1
  print(f"\n\nFinish filling the memory, total fill {row} rows.")

def sram_request_reciever (single_request):
  current_dim = single_request[0]
  weight_bits = single_request[1]
  in_weight   = single_request[2]

def create_single_request(prior_dim, in_weight):
  weight_bits = 4
  single_request = (prior_dim, weight_bits, in_weight) #* Current format of request info: (# of current col or pump dimension, weight_bitwidth, number of weights requested)
  weight_left = sram_request_reciever(single_request)
  return weight_left

def set_matrix_read_request_weight(self, matrix_weight):

    #* matrix_weight is the weight matrix, should be a 2D list to indicate the weight matrix size.

    S_c = matrix_weight[1] #! Need to check the dimension, 0 or 1?
    S_p = matrix_weight[0] #! Need to check the dimension, 0 or 1?

    traverse_order = 'p' #! Allow the user to set the traverse order.
    
    #* Tranverse the weight matrix, by having 'p' dimension prioritized, each SRAM line is filled by elements from one column first.
    if traverse_order == 'p':
        for col in range(S_c):
          weight_left = create_single_request(col, S_p)
          while weight_left > 0:
             weight_left = create_single_request(col, weight_left)
          
    #* By having 'c' dimension prioritized, each SRAM line is filled by elements from one row first.
    else:
        for row in range(S_p):
            create_single_request()
            
    return 


