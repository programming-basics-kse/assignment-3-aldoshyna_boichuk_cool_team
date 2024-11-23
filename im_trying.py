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

    country = medals[0]
    year = medals[1]
    output_list = []               #[winners_name, sport, medal_type]
    counter_country = 0
    counter_year = 0
    for row in rows:
        if row[COUNTRY]==country or row[NOC]==country:
            counter_country += 1
            if row[YEAR]==year:
                counter_year += 1
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



parser=argparse.ArgumentParser()
parser.add_argument("fileName", type=str, help="getting name of file to work with")
parser.add_argument("-medals", nargs=2, help="getting the country and year")
parser.add_argument("-output", action='store', help="getting name of file to output information", dest='output')
parser.add_argument("-total", type=str, help="getting the year to count total")
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


