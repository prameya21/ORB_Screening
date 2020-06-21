import re

def clean_names(rawData):
    ret=[]
    pattern='d+\W*b+\W*a\W'
    for data in rawData:
        #x=re.search(pattern,data,re.IGNORECASE)
        result=re.split(pattern,data,flags=re.IGNORECASE)
        result=parse(result)
        if len(result)==1:
            result.append(None)
            ret.append(tuple(result))
        else:
            ret.append(tuple(result))

    return ret


def parse(data):
    result=[]
    for d in data:
        pattern='\A\W*'
        replace=''
        d=re.sub(pattern,replace,d)
        pattern='\W*\Z'
        d=re.sub(pattern,replace,d)
        d=re.sub('_',' ', d)
        result.append(d.strip())
    return result




if __name__=="__main__":

    CLEANED_NAME_PAIRS = [('SPV Inc', 'Super Company'),('Michael Forsky LLC', 'F/B Burgers'),('Youthful You Aesthetics', None),('Aruna Indika', 'NGXess'),('Diot SA', 'Diot-Technologies'),('PERFECT PRIVACY, LLC', 'Perfection'),('PostgreSQL DB Analytics', None),('JAYE INC', None),('ETABLISSEMENTS SCHEPENS', 'ETS SCHEPENS'),('DUIKERSTRAINING OOSTENDE', 'D.T.O'),]
    rawData=['SPV Inc., DBA: Super Company',
             'Michael Forsky LLC d.b.a F/B Burgers .',
             '*** Youthful You Aesthetics ***',
             'Aruna Indika (dba. NGXess)',
             'Diot SA, - D. B. A. *Diot-Technologies*',
             'PERFECT PRIVACY, LLC, d-b-a Perfection,',
             'PostgreSQL DB Analytics',
             '/JAYE INC/',
             ' ETABLISSEMENTS SCHEPENS /D.B.A./ ETS_SCHEPENS',
             'DUIKERSTRAINING OOSTENDE | D.B.A.: D.T.O. ']
    #print(clean_names(rawData))


    assert clean_names(rawData) == CLEANED_NAME_PAIRS


