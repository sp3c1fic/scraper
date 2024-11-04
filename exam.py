def scam():
    money = float(input())
    users = int(input())
    index = 1
    total_money = 0

    index = 1

    for i in range(index, users + 1):
        user_searches = int(input())
        if user_searches == 1: continue
        if i % 3 == 0:
            earned = money * user_searches * 3
            if user_searches > 5:
                earned *= 2
            total_money += earned
        else:
            if user_searches > 5:
                total_money += money * user_searches * 2
            else:
                total_money += money * user_searches

    print('Total money earned: %.2f' % total_money)

def read_book():
    books = input().split(" | ")

    while True:

        cmd = input()
        if cmd.lower() == "stop!": break

        split_cmd = cmd.split(" ")
        action = split_cmd[0]
        
        if action.lower() == "join":
            genre = split_cmd[1]
            if genre not in books:
                books.append(genre)
        elif action.lower() == "drop":
            genre = split_cmd[1]
            if genre not in books: continue
            books.remove(genre)
        elif action.lower() == "replace":
            old_genre = split_cmd[1]
            new_genre = split_cmd[2]

            if old_genre in books and new_genre not in books:
                index = books.index(old_genre)
                books[index] = new_genre
        elif action.lower() == "prefer":
            first_index = int(split_cmd[1])
            second_index = int(split_cmd[2])

            if first_index < 0 or first_index >= len(books) or second_index < 0 or second_index >= len(books):
                continue
            
            temp = books[first_index]
            books[first_index] = books[second_index]
            books[second_index] = temp

    print(" ".join(books))

def paint():
    paintings = list(map(int, input().split()))

    while True:
        cmd = input()
        if cmd.upper() == "END":
            break
        
        split_cmd = cmd.split()
        action = split_cmd[0]

        if action.lower() == "change":
            old_num = int(split_cmd[1])
            new_num = int(split_cmd[2])
            if old_num in paintings:
                old_num_index = paintings.index(old_num)
            paintings[old_num_index] = new_num
        elif action.lower() == "hide":
            num = int(split_cmd[1])
            if num in paintings:
                paintings.remove(num)
        elif action.lower() == "switch":
            first_number = int(split_cmd[1])
            second_number = int(split_cmd[2])

            if first_number in paintings and second_number in paintings:
                first_number_index = paintings.index(first_number)
                second_number_index = paintings.index(second_number)

                # Swapping using tuple unpacking
                paintings[first_number_index], paintings[second_number_index] = (
                    paintings[second_number_index], 
                    paintings[first_number_index]
                )
            
        elif action.lower() == "insert":
            index = int(split_cmd[1])
            num = int(split_cmd[2])
            
            if index >= 0 and index < len(paintings) - 1:
                paintings.insert(index + 1, num)
        elif action.lower() == "reverse":
            paintings = paintings[::-1]
            
    print(" ".join(map(str, paintings)))

if __name__ == "__main__":
    paint()
