
def printCompetitor(competitor):
    '''
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']
    
    print(f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries 
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if country != undef_country]
    print(f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    '''
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format: 
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name,result)


def readParseData(file_name):
    '''
    Given a file name, the function returns a list of competitors.
    Arguments: 
        file_name: the input file name. Assume that the input file is in the directory of this script.
    Return value:
        A list of competitors, such that every record is a dictionary, in the following format:
            {'competition name': competition_name, 'competition type': competition_type,
                'competitor id': competitor_id, 'competitor country': competitor_country, 
                'result': result}
    '''
    #each line starts with a header- competitor or competition
    line_header=0
    competitor_id_place=1
    competitor_country_place=2
    competition_id_place=1 
    competition_result_place=3
    competitors_in_competitions = []#list of all the competirots in the games
    competitors={}#dict of all the the competitors in the games
    defult_competition=['competition name','competitor id','competition type','result']
    with open(file_name,'r') as file:
        lines= file.readlines()
    for line in lines:
        cur_line_list=line.split(' ') 
        if cur_line_list[line_header]=='competitor': #line describe a competitor
        #line structure: competitor <competitor id> <competitor country>
            cur_line_list[competitor_country_place]=cur_line_list[competitor_country_place][0:len(cur_line_list[competitor_country_place])-1]
            cur_line_list[competitor_id_place]=int(cur_line_list[competitor_id_place])-int('0')
            competitors[cur_line_list[competitor_id_place]]=cur_line_list[competitor_country_place]
        else: #line describe a competition
        #competition <competition name> <competitor id> <competition type> <result>
            competition={} 
            cur_line_list.remove('competition')
            cur_line_list[competition_id_place]=int(cur_line_list[competition_id_place])-int('0')#cast id to int
            cur_line_list[competition_result_place]=int(cur_line_list[competition_result_place])-int('0')#cast result to int
            for i,element in enumerate(cur_line_list):
                competition[defult_competition[i]]=element
            competitors_in_competitions.append(competition)
    for competition_dict in competitors_in_competitions: #run on all the compitions and add them the countery of each competitor
        competition_dict['competitor country']=competitors[competition_dict['competitor id']] #get an id of a competitor and return the country he represented 
    return sorted(competitors_in_competitions,key=key_sort_competitor)

def isBigger(a,b):
    if a>b:
        return True
    return False

def isSmaller(a,b):
    if a<b:
        return True
    return False


def compitedMoreThanOnce(competitors_in_competitions,competitor):
    '''
    get a list of all the competitors in the games and check if a competitor 
    participated in more then one game return true if he did, false otherwise
    '''
    count=0
    invalid_number_of_games=2
    for element in competitors_in_competitions:
        if count==invalid_number_of_games:
            return True
        if element['competitor id']==competitor['competitor id']:
            count+=1
    if count==invalid_number_of_games:
            return True
    return False

def calcWinners(list_of_competitors_in_one_competition, compareCondition):
    '''
    gets a list of competiotors in one competition and return the a list
    the first item is the name of the competition, the first, second and third places
    '''
    header=0
    first_country='undef_country'
    second_country='undef_country'
    third_country='undef_country'
    first_result=-1
    second_result=-1
    third_result=-1
    for element in list_of_competitors_in_one_competition:
        if compitedMoreThanOnce(list_of_competitors_in_one_competition,element):
            continue #competitor is excluded from games for participating more than one time
        if first_result==-1 or compareCondition(element['result'],first_result):#found a new first 
            tmp=second_result#swap third and second results
            second_result=third_result
            third_result=tmp

            tmp=first_result#swap second and first results
            first_result=second_result
            first_result=tmp
            
            first_result=element['result']
            
            tmp_str=second_country#swap third and second country
            second_country=third_country
            third_country=tmp_str

            tmp_str=first_country#swap first and second country
            first_country=second_country
            second_country=tmp_str
            
            first_country=element['competitor country']

        elif second_result==-1 or compareCondition(element['result'],second_result):#found a new second
            tmp=third_result#swap third and second results
            third_result=second_result
            second_result=tmp

            second_result=element['result']

            tmp_str=third_country#swap third and second country
            third_country=second_country
            second_country=tmp_str

            second_country=element['competitor country']

        elif third_result==-1 or compareCondition(element['result'],third_result):#found a new third
            third_result=element['result']
            third_country=element['competitor country']
    return [(list_of_competitors_in_one_competition[header])['competition name'],first_country, second_country,third_country]
    


def timedWinners(list_of_competitors_in_one_competition):
    '''
    call the winners by the lowest result
    '''
    return calcWinners(list_of_competitors_in_one_competition, isSmaller)
def untimedWinners(list_of_competitors_in_one_competition):
    '''
    call the winners by the longest result
    '''
    return calcWinners(list_of_competitors_in_one_competition, isBigger)
def knockoutWinners(list_of_competitors_in_one_competition):
    '''
    call the winners by being in the top of the calssificatin
    '''
    return calcWinners(list_of_competitors_in_one_competition, isSmaller)

def calcCompetitionsResults(competitors_in_competitions):
    '''
    Given the data of the competitors, the function returns the champs countries for each competition.
    Arguments:
        competitors_in_competitions: A list that contains the data of the competitors
                                    (see readParseData return value for more info)
    Retuen value:
        A list of competitions and their champs (list of lists). 
        Every record in the list contains the competition name and the champs, in the following format:
        [competition_name, winning_gold_country, winning_silver_country, winning_bronze_country]
'''
    winners_list_in_one_comp=[]
    competitions_champs = []
    i=0
    length=len(competitors_in_competitions)
    while(i<length):
        count=1
        curr_comp_name=(competitors_in_competitions[i])['competition name']
        curr_comp_type=(competitors_in_competitions[i])['competition type']
        while(i+count<length and (competitors_in_competitions[i+count])['competition name']==curr_comp_name):
            count+=1
        if curr_comp_type=='timed':
            winners_list_in_one_comp=timedWinners(competitors_in_competitions[i:i+count])
        elif curr_comp_type=='untimed':
            winners_list_in_one_comp=untimedWinners(competitors_in_competitions[i:i+count])
        elif curr_comp_type=='knockout':
            winners_list_in_one_comp=knockoutWinners(competitors_in_competitions[i:i+count])
        competitions_champs.append(winners_list_in_one_comp)
        i+=count 
    return competitions_champs

def partA(file_name = 'input.txt', allow_prints = True):
    # read and parse the input file
    competitors_in_competitions = readParseData(file_name)
    if allow_prints:
        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)

    # calculate competition results
    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)
    return competitions_results

def partB(file_name = 'input.txt'):
    import Olympics
    competitions_results = partA(file_name, allow_prints = False)
    olympics = Olympics.OlympicsCreate()
    first_place=1
    second_place=2
    third_place=3
    for elements in competitions_results:
        gold=elements[first_place]
        silver=elements[second_place]
        bronze=elements[third_place]
        Olympics.OlympicsUpdateCompetitionResults(olympics,str(gold),str(silver),str(bronze))
    Olympics. OlympicsWinningCountry(olympics)
    Olympics.OlympicsDestroy(olympics)

if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.
    
    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''    
    file_name = 'input.txt'
    partA(file_name)
    partB(file_name)