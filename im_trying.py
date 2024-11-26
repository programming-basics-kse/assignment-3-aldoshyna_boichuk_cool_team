import csv
import argparse


def opening_file(fileName):
    with open(fileName, "r") as file:
        csv_reader = csv.reader(file, delimiter='\t')
        header = next(csv_reader)
        rows = []
        for line in csv_reader:
            rows.append(line)
    return header, rows


def country_input_check(rows, COUNTRY, NOC, countries):
    all_countries_and_codes_list = []
    for row in rows:
        if not row[COUNTRY] in all_countries_and_codes_list:
            all_countries_and_codes_list.append(row[COUNTRY])
        if not row[NOC] in all_countries_and_codes_list:
            all_countries_and_codes_list.append(row[NOC])
    for country in countries:
        if not country in all_countries_and_codes_list:
            index_country = countries.index(country)
            for i in range(index_country+1, len(countries)):
                new_country = " ".join(countries[index_country:i+1])
                if new_country in all_countries_and_codes_list:
                    countries[index_country] = new_country
                    for j in range(index_country+1, i+1):
                        countries.pop(j)
    return countries


def counting_medals_1(output_list, country, year):
    gold_medals = 0
    silver_medals = 0
    bronze_medals = 0
    for winner in output_list:
        if winner[2] == "Gold":
            gold_medals += 1
        elif winner[2] == "Silver":
            silver_medals += 1
        elif winner[2] == "Bronze":
            bronze_medals += 1
    print("\nOverall {} in {} got: \nGold medals: {} \nSilver medals: {} \nBronze medals: {} \n".format(country, year, gold_medals, silver_medals, bronze_medals))
    return output_list


def medals_1(fileName, medals):
    header, rows = opening_file(fileName)
    COUNTRY = header.index('Team')
    YEAR = header.index('Year')
    NAME = header.index('Name')
    SPORT = header.index('Sport')
    MEDAL = header.index('Medal')
    NOC = header.index('NOC')
    top_medals = ["Gold", "Silver", "Bronze"]

    country = country_input_check(rows, COUNTRY, NOC, medals[:-1])[0]
    year = medals[-1]
    output_list = []               #[winners_name, sport, medal_type]
    counter_country = 0
    counter_year = 0
    for row in rows:
        if row[COUNTRY]==country or row[NOC]==country:
            counter_country += 1
            if row[YEAR]==year:
                counter_year += 1
                if row[MEDAL] in top_medals:
                    output_list.append([row[NAME], row[SPORT], row[MEDAL]])
    if counter_country==0:
        print("\nSorry! There is no information about {} country in our dataset.".format(country))
        return 0
    if counter_year==0:
        print("\nSorry! There is no information about {} country in {} year in our dataset.".format(country, year))
        return 0
    elif len(output_list)==0:
        print("\nSorry! There were no Olympic winners from {} in {}.".format(country, year))
        return 0
    elif len(output_list)<10:
        print("\nSorry! There were only {} Olympic winners from {} in {}.\n".format(len(output_list), country, year))
        for winner in output_list:
            print("{} - {} - {}".format(winner[0], winner[1], winner[2]))
        return counting_medals_1(output_list, country, year)
    else:
        for winner in output_list[:10]:
            print("{} - {} - {}".format(winner[0], winner[1], winner[2]))
        return counting_medals_1(output_list, country, year)


def total_2(fileName, year):
    header, rows = opening_file(fileName)
    COUNTRY = header.index('Team')
    YEAR = header.index('Year')
    MEDAL = header.index('Medal')
    top_medals = ["Gold", "Silver", "Bronze"]
    total_counter = {}            #country : [num_gold_medals, num_silver_medals, num_bronze_medals]
    for row in rows:
        if row[YEAR]==year and row[MEDAL] in top_medals:

            if not row[COUNTRY] in total_counter:
                total_counter[row[COUNTRY]] = [0, 0, 0]
            medal = row[MEDAL]
            total_counter[row[COUNTRY]][top_medals.index(medal)] += 1
    if total_counter=={}:
        print("\nSorry! There is no information about {} year in our dataset.".format(year))
    else:
        for country in total_counter.items():
            print("{:<15} -- Gold: {} -- Silver: {} -- Bronze: {}".format(country[0], country[1][0], country[1][1], country[1][2]))


def overall_3(fileName, countries):
    header, rows = opening_file(fileName)
    COUNTRY = header.index('Team')
    YEAR = header.index('Year')
    NOC = header.index('NOC')
    MEDAL = header.index('Medal')
    top_medals = ["Gold", "Silver", "Bronze"]
    countries = country_input_check(rows, COUNTRY, NOC, countries)
    overall_counter = {}
    for country in countries:
        for row in rows:
            if row[COUNTRY] == country or row[NOC] == country:
                if row[MEDAL] in top_medals:
                    if country in overall_counter:
                        if row[YEAR] in overall_counter[country]:
                            # print(row)
                            overall_counter[country][row[YEAR]] += 1
                            # print(row[1], row[COUNTRY], row[MEDAL])
                        else:
                            overall_counter[country][row[YEAR]] = 1
                    else:
                        overall_counter[country] = {}
                        overall_counter[country][row[YEAR]] = 1
    for country in countries:
        if country in overall_counter:
            country_medals = overall_counter[country]
            top_year = sorted(country_medals.items(), key=lambda x: x[1], reverse=True)[0]
            print("{}: \n \tyear: {}, number of medals: {}".format(country, top_year[0], top_year[1]))
        else:
            print("\nSorry! There is no information about {} country in our dataset.".format(country))


def country_is_valid_4(rows, COUNTRY, NOC, country):
    all_countries_and_codes_list = []
    for row in rows:
        if not row[COUNTRY] in all_countries_and_codes_list:
            all_countries_and_codes_list.append(row[COUNTRY])
        if not row[NOC] in all_countries_and_codes_list:
            all_countries_and_codes_list.append(row[NOC])
    if not country in all_countries_and_codes_list:
        return False
    return True


def first_olympiad_4(rows, COUNTRY, NOC, YEAR, CITY, country):
    first_olympiad_list = []  # [year, city]
    for row in rows:
        if row[COUNTRY] == country or row[NOC] == country:
            if not [row[YEAR], row[CITY]] in first_olympiad_list:
                first_olympiad_list.append([row[YEAR], row[CITY]])
    first_olympiad = sorted(first_olympiad_list, key=lambda x: x[0])[0]
    print(f"\nThe first time {country} participated in Olympics was in {first_olympiad[0]} in {first_olympiad[1]}.")


def best_and_worst_olympiad_4(rows, COUNTRY, NOC, YEAR, MEDAL, country):
    top_medals = ["Gold", "Silver", "Bronze"]
    successful_olympiad_dict = {}   # year: gold, silver, bronze, total num of medals -> sort -> pick the most successful and the least
    for row in rows:
        if (row[COUNTRY] == country or row[NOC] == country) and row[MEDAL] in top_medals:
            if not row[YEAR] in successful_olympiad_dict:
                successful_olympiad_dict[row[YEAR]] = [0, 0, 0, 0]
            successful_olympiad_dict[row[YEAR]][top_medals.index(row[MEDAL])] += 1
            successful_olympiad_dict[row[YEAR]][3] += 1

    successful_olympiad_dict = sorted(successful_olympiad_dict.items(), key=lambda x: x[1][3])
    most_successful_olympiad = [x for x in successful_olympiad_dict if x[1][3] == successful_olympiad_dict[-1][1][3]]
    most_successful_olympiad_sorted = ", ".join(sorted([x[0] for x in most_successful_olympiad]))
    least_successful_olympiad = [x for x in successful_olympiad_dict if x[1][3] == successful_olympiad_dict[0][1][3]]
    least_successful_olympiad_sorted = ", ".join(sorted([x[0] for x in least_successful_olympiad]))
    print(
        f"\nThe most successful olympiad of {country} was in {most_successful_olympiad_sorted} when it got {most_successful_olympiad[0][1][3]} medals in total.")
    print(
        f"\nThe least successful olympiad of {country} was in {least_successful_olympiad_sorted} when it got {least_successful_olympiad[0][1][3]} medals in total.")
    return successful_olympiad_dict


def average_num_medals_4(successful_olympiad_dict, country):
    medals_total_list = [0, 0, 0]
    for year in successful_olympiad_dict:
        medals_total_list[0] += year[1][0]
        medals_total_list[1] += year[1][1]
        medals_total_list[2] += year[1][2]
    print(f"\nThe average number of medals that {country} got on each Olympiad is: "
          f"\nGold: {round((medals_total_list[0] / len(successful_olympiad_dict)), 1)} ({medals_total_list[0]} in total)"
          f"\nSilver: {round((medals_total_list[1] / len(successful_olympiad_dict)), 1)} ({medals_total_list[1]} in total)"
          f"\nBronze: {round((medals_total_list[2] / len(successful_olympiad_dict)), 1)} ({medals_total_list[2]} in total)")


def interactive_4(fileName):
    print("\nYou've switched to interactive mode!")
    header, rows = opening_file(fileName)
    COUNTRY = header.index('Team')
    YEAR = header.index('Year')
    CITY = header.index('City')
    NOC = header.index('NOC')
    MEDAL = header.index('Medal')

    country = input("Enter the name or code of country you want to find out more about: ")
    while not country_is_valid_4(rows, COUNTRY, NOC, country):
        country = input(
            "Sorry, this isn't a proper name or code of country. Try again. \nEnter the name or code of country you want to find out more about: ")

    first_olympiad_4(rows, COUNTRY, NOC, YEAR, CITY, country)

    successful_olympiad_dict = best_and_worst_olympiad_4(rows, COUNTRY, NOC, YEAR, MEDAL, country)

    average_num_medals_4(successful_olympiad_dict, country)


def top(fileName, arguments):
    header, rows = opening_file(fileName)
    MEDAL = header.index('Medal')
    SEX = header.index('Sex')
    AGE = header.index('Age')
    NAME = header.index('Name')
    arguments1 = []
    arguments2 = []
    for i in arguments:
        if i.isalpha():
            arguments1.append(i)
        elif i.isdigit():
            arguments2.append(i)
    if arguments2 == [] or arguments1== []:
        print('Please enter sex in form of "M" or "F", and age range: ')
        return False
    top_medals = ["Gold", "Silver", "Bronze"]
    age_dic = {1:[*range(18,25,1)], 2:[*range(25,35,1)], 3:[*range(35,50,1)], 4:[*range(50,150,1)]}
    overall_players = {}
    for i in arguments1:
        for j in arguments2:
            for row in rows:
                if row[AGE] == 'NA':
                    continue
                if row[SEX] == i and int(row[AGE]) in age_dic[int(j)] and row[MEDAL] in top_medals:
                    if row[NAME] in overall_players:
                        overall_players[row[NAME]]+=1
                    else:
                        overall_players[row[NAME]] = 1
            top_player = sorted(overall_players.items(), key=lambda x: x[1], reverse=True)[0]
            print(top_player)
            overall_players = {}




parser=argparse.ArgumentParser()
parser.add_argument("fileName", type=str, help="getting name of file to work with")
parser.add_argument("-medals", nargs='+', help="getting the country and year")
parser.add_argument("-output", action='store', help="getting name of file to output information", dest='output')
parser.add_argument("-total", type=str, help="getting the year to count total")
parser.add_argument("-overall", nargs='+', help="getting multiple names of countries")
parser.add_argument("-interactive", action="store_true", help="switching to interactive mode")
parser.add_argument("-top", nargs='+', help="getting multiple names of countries")
args=parser.parse_args()


if args.medals:
    result = medals_1(args.fileName, args.medals)
    if args.output and result!=0:
        with open(args.output, 'a') as file_output:
            for i in result:
                file_output.write(str(i))
            file_output.write('\n')
if args.total:
    total_2(args.fileName, args.total)
if args.overall:
    overall_3(args.fileName, args.overall)
if args.interactive:
    interactive_4(args.fileName)
if args.top:
    top(args.fileName, args.top)

