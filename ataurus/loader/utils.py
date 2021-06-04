def get_sublists(main_list: list, count: int):
    """
    Function splits the main list to $count sublists: extra elements will be appended into the first sublists.
    :param main_list: a list that will be split
    :param count: count of sublists
    :return: list of sublists
    """
    if not main_list:
        return [[]]

    # Minimal count of elements per sublist
    count_per_list = len(main_list) // count

    # If count of elements more or equal count of sublists
    if count_per_list != 0:
        # Split the main list to 2 parts
        rest_list = main_list[count * count_per_list:]
        main_list = main_list[:count * count_per_list]

        sublists = [main_list[x:x + count_per_list] for x in range(0, len(main_list), count_per_list)]

        # Append extra elements into the first sublists
        for index, element in enumerate(rest_list):
            sublists[index].append(element)
    # If count of elements less than count of sublists
    else:
        sublists = [main_list[x:x + 1] for x in range(0, len(main_list))]

    return sublists
