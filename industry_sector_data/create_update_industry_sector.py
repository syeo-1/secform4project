'''
uses yahoo finance api to create a table of data with info about stock tickers and the industry
and sectors that they belong in
'''
import requests
import yfinance as yf
from config import *
import psycopg2

TICKER_URL = 'http://localhost:8000/api/common/all_tickers'

SECTOR_INDUSTRY_TABLE_STATEMENT = '''
    CREATE TABLE IF NOT EXISTS
    sector_industry
    (
    sector_industry_id SERIAL,
    company_name TEXT NULL,
    ticker_symbol TEXT,
    sector TEXT,
    industry TEXT,
    PRIMARY KEY(company_name, ticker_symbol, sector, industry),
    CONSTRAINT sector_constraint UNIQUE (company_name, ticker_symbol, sector, industry)
    );
'''

def store_or_update_tables():
    '''
        read from the generated file from get_industry_sector_data

        input into the database the sector and industry data
    '''
    table_name = 'sector_industry'
    columns = f'''
        company_name,
        ticker_symbol,
        sector,
        industry
    '''
    connection = psycopg2.connect(f'dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={HOST}')
    cursor = connection.cursor()
    try:
        cursor.execute(SECTOR_INDUSTRY_TABLE_STATEMENT)
        print('Sector table successfully generated')
    except psycopg2.Error as postgres_table_creation_error:
        print(f'Error in generating sector table in postgres: {postgres_table_creation_error}')
        exit(1)
    # read the file
    # with open('ticker_sector_data.txt', 'r', encoding='utf-16') as file:
    with open('ticker_sector_data.txt', 'r', encoding='utf-16') as file:
        for line in file:
            line_data = line.rstrip().split('|')
            company_name = line_data[0] if line_data[0] != 'None' else None
            ticker = line_data[1] if line_data[1] != 'None' else None
            sector = line_data[2] if line_data[2] != 'None' else None
            industry = line_data[3] if line_data[3] != 'None' else None

            if sector == None and industry == None:
                continue

            try:
                cursor.execute(f'''
                    INSERT INTO {table_name}({columns}) values(
                    %s,
                    %s,
                    %s,
                    %s
                    ) ON CONFLICT (company_name, ticker_symbol, sector, industry) DO NOTHING
                ''', tuple([company_name, ticker, sector, industry]))
                print(f'query to insert sector data is successful')
            except psycopg2.Error as postgres_insert_error:
                print(f'error in inserting sector data into postgres table: {postgres_insert_error}')
            except ValueError as value_error:
                print(f'value error occured: {value_error}')
            except TypeError as type_error:
                print(f'type error occured: {type_error}')
            except Exception as e:
                print(f'general error occured: {e}')
        
            connection.commit()

    connection.close()
    cursor.close()



    # load each row of data to the database



def get_industry_sector_data():
    '''
    retrieve which industry and sector a company belongs to
    '''

    # use own api to get ticker information
    all_tickers = requests.get(TICKER_URL).json()
    error_causing_tickers = ['JUSH/JUSHF', 'UONE/UONEK', 'NYSE/TRN', 'MOGA/MOGB', 'GTII/GTBIF', 'N/A', 'FRTX', 'RZLT', 'AADI', 'PSX', 'HRL', 'CPRT', 'MKL', 'BMEA', 'DLPN', 'KPRX', 'BRST', 'AGR', 'TMRC', 'PLXS', 'SMA', 'AVGR', 'KNSL', 'WHD', 'MRVL', 'BYM', 'FLL', 'FNB', 'GHSI', 'SDHC', 'TCBC', 'SQSP', 'MUSA', 'M', 'TTI', 'AZPN', 'OLN', 'DTM', 'ALTR', 'MGY', 'CAG', 'FLGC', 'AMWL', 'TMHC', 'EHC', 'BHR', 'IGMS', 'JMSB', 'DNP', 'NASDAQ:FVE', 'CGBD', 'AVO', 'EXPE', 'RAPP', 'GH', 'BOXL', 'NEXT', 'WHR', 'vicr', 'NRT', 'HYLN', 'BGT', 'SUPN', 'WMS', 'HBCP', 'PYCR', 'SHOO', 'FBP', 'NFG', 'PWOD', 'META', 'RXT', 'LFCR', 'LRFC', 'CCL', 'VSTM', 'DO', 'IOT', 'ALDX', 'IPG', 'LWAY', 'CAVA', 'R', 'TBBK', 'OGS', 'SHEN', 'ROAD', 'BOKF', 'ISGR', 'LODE', 'WSM', 'UHAL,UHALB', 'USLM', 'AEP', 'RLI', 'RGP', 'MCBS', 'TNDM', 'MG', 'F', 'TXMD', 'H', 'BKNG', 'AARD', 'OPCH', 'MCB', 'VEEV', 'SLDB', 'ECPG', 'KFS', 'BGXX', 'NFLX', 'SANA', 'IFN', 'ESS', 'MANH', 'ESCA', 'RPM', 'CVX', 'TDC', 'CFFN', 'VKTX', 'NET', 'HTBI', 'DHY', 'UDMY', 'ONB', 'PSN', 'WY', 'utgn', 'STRUX', 'SER', 'RUM', 'CBAN', 'SSB', 'TNET', 'BMY', 'EQ', 'HIW', 'STTK', 'BSM', 'BGC', 'SDIG', 'CET', 'VIVK', 'ALRN', 'TXO', 'NLY', '(SIRI)', 'NASDAQ:DHC', 'MTW', 'OPXS', 'AXNX', 'INSG', 'XRX', 'EVR', 'USPH', 'BMN', 'OPOF', 'UUUU', 'CLSR', 'NPCE', 'AKBA', 'ARR', 'FTDR', 'APP', 'NTIC', 'INSW', 'LADR', 'GWAV', 'ULCC', 'AHNR', 'UI', 'ARTV', 'SMR', 'MONIX', 'VNT', 'GOOGL', 'INN', 'ATII', 'WDI', 'FREY', 'LOOP', 'BKR', 'MTH', 'WINA', 'PBH', 'AXP', 'BIO BIO.B', 'EDIT', 'GEN', 'CING', 'ESP', 'FERA', 'ADC', 'CSQ', 'CRNX', 'MGRX', 'GWRE', 'ATKR', 'CCOI', 'EDR', 'PKG', 'PBYI', 'MFIC', 'PRIM', 'RRBI', 'PB', 'SHW', 'TDOC', 'MBBC', 'SXTP', 'PLAB', 'GATX', 'COFS', 'NGNE', 'K', 'RPD', 'ATYR', 'SYM', 'GRWG', 'AUMN', 'APLD', 'AEO', 'LPLA', 'LBRT', 'FANG', 'SEI', 'SG', 'EWBC', 'NREF', 'WSR', 'TRUP', 'BLND', 'SRM', 'LLIAX', 'AKYA', 'PRT', 'OWLT', 'FRD', 'AVB', 'SES', 'SJM', 'SYBT', 'FG', 'LAMR', 'WLKP', 'NRGV', 'BWFG', 'OCUL', 'EXEL', 'MDXG', 'BRTX', 'IBCP', 'ENSG', 'GLDD', 'ALHC', 'FSEA', 'CBT', 'PNR', 'RVNC', 'REYN', 'MMD', 'AMRC', 'APPN', 'LKQ', 'MUX', 'NTAP', 'NX', 'AMTM', 'ALLO', 'TRC', 'KRRO', 'LNW', 'IBP', 'TMQ', 'DBD', 'DHCIX', 'PMN', 'JAKK', 'AYTU', 'TZOO', 'BEN', 'BXP', 'NCMI', 'FFIV', 'AL', 'GRYP', 'PAYX', 'ADM', 'CSTL', 'LC', 'AYI', 'ICFI', 'BXSY', 'MPB', 'WNEB', 'XNCR', 'STRW', 'NWBI', 'FLR', 'CNTM', 'DRQ', 'OXM', 'OCFC', 'GTI', 'CMG', 'PDFS', 'FORR', 'SOUN', 'SACH', 'DUK', 'MODD', 'CPTN', 'NUTX', 'TCMD', 'VRRM', 'TRU', 'NEO', 'OKLO', 'III', 'ATLO', 'TSBK', 'MAMO', 'TROW', 'MTTR', 'TENB', 'DHI', 'ATUS', 'GIPR', 'BECN', 'MTB', 'CMPS', 'ROCL', 'NUVB', 'ISSC', 'ALGN', 'SSNT', 'none', 'QMCO', 'HAE', 'IFF', 'GS', 'GSBC', 'STRL', 'JOBY', 'CFLT', 'ASUR', 'COYA', 'CRNC', 'BASE', 'SOPA', 'BC', 'BLBD', 'AIRG', 'KZR', 'CORZ', 'RNR', 'SND', 'RNXT', 'SLRC', 'VNDA', 'STER', 'VIRT', 'SHLS', 'DDOG', 'MTN', 'GRST', 'IPW', 'ARDX', 'LPRO', 'AGD', 'PCVX', 'xpl', 'BCML', 'SIG', 'CWD', 'CHWY', 'NVEE', 'UPLD', 'RCG', 'NPKI', 'VYNE', 'PET', 'WBS', 'MEGI', 'QTWO', 'IZTC', 'DG', 'NVCR', 'AGX', 'SCISX', 'THRD', 'HSY', 'UMAC', 'SW', 'MIRA', 'EBF', 'MSGE', 'JNPR', 'SNA', 'AXR', 'TURN', 'FAF', 'STZ', 'LIVN', 'MSTR', 'OGEN', 'COLD', 'DFH', 'VCYT', 'LHX', 'HNNA', 'PACB', 'ZOMDF', 'PARAA,PARA', 'ZS', 'DXC', 'MPAA', 'LEXX', 'LBTYK', 'INVE', 'SRPT', 'LEG', 'XHFIX', 'EBTC', 'DEA', 'REX', 'BY', 'BUSE', 'EPR', 'STRR', 'SPRO', 'GTHX', 'SONX', 'CAPR', 'JCI', 'PSQH', 'SEDG', 'TWLO', 'MCAGU', 'PRAA', 'FAT', 'BOX', 'ARHS', 'HRZN', 'BLNK', 'RMMZ', 'DTST', 'WABC', 'PBF', 'WBTN', 'CRDA CRDB', 'QCOM', 'EVBN', 'SOAR', 'PLSE', 'MBC', 'CHCI', 'CCSI', 'CVLT', 'AWR', 'WAY', 'NWTOU', 'BKSY', 'TPR', 'GLP', 'APLS', 'GOEV', 'MC', 'APOG', 'VRTX', 'HASI', 'NXPI', 'ORGO', 'CCBG', 'SPWH', 'BBW', 'KEY', 'PWR', 'AWIN', 'PRTH', 'ATOS', 'ETR', 'ROP', 'KF', 'CNO', 'BHC', 'ALDF', 'TW', 'CAR', 'EQT', 'LIDR', 'OUST', 'TMDX', 'HAFC', 'EFSI', 'BLIN', 'BYND', 'LDOS', 'FSK', 'RDZN', 'BOW', 'VALF', 'THAR', 'BKKT', 'ALLY', 'PPG', 'TTD', 'QS', 'SERV', 'FSHP', 'LUXH', 'HXL', 'CPSH', 'ATAI', 'BOH', 'ALTI', 'JKHY', 'ESNT', 'RLAY', 'TAKMX', 'APTO', 'NAVI', 'UPB', 'CDP', 'RIG', 'NXG', 'LEN, LEN.B', 'NXPL', 'SNYR', 'NKE', 'CODA', 'MRNS', 'ZONE', 'ALSN', 'CC', 'TCBK', 'EBAY', 'XAIR', 'FTV', 'GLAD', 'TNGX', 'ATXG', 'EVT', 'XCUR', 'OSPN', 'PWP', 'NRIM', 'emby', 'TRUE', 'DVAX', 'KYMR', 'SRBK', 'APA', 'FORM', 'HLIO', 'FKYS', 'RBKB', 'MHLD', 'LNSR', 'O', 'ULTA', 'BRCC', 'APPS', 'FRME', 'UVSP', 'VAC', 'HOTH', 'WMT', 'MBIN', 'FLWS', 'ALTM', 'A', 'CHD', 'AEIS', 'GAIAX', 'LDI', 'PFLT', 'SFBC', 'QBTS', 'FVCB', 'GBCI', 'CRWD', 'MLYS', 'CRVL', 'ASRV', 'CSPI', 'APD', 'LCII', 'WSBC', 'HLNE', 'AVNW', 'GSIT', 'CLAR', 'PRGO', 'LCLC', 'LFST', 'ITOS', 'HTLD', 'CRH', 'HSTM', 'MINM', 'RNGR', 'DKL', 'EQBK', 'RMD', 'SGH', 'NKLA', 'ETSY', 'DOCU', 'ZIP', 'PAPL', 'MPLN', 'GNTX', 'DMLP', 'KO', 'NOTV', 'TKR', 'XPEL', 'EA', 'SCVL', 'CELH', 'SRTS', 'IRTC', 'ELAN', 'FDP', 'TASK', 'LTC', 'DGICA', 'GCBC', 'HKHC', 'NBY', 'OTIS', 'BTO', 'GD', 'WOLF', 'BLSK', 'FICO', 'AREN', 'CAH', 'COIN', 'TRGP', 'RVP', 'INMB', 'GECC', 'SNCR', 'CCI', 'RBA', 'MGX', 'EVER', 'GEHC', 'HD', 'VSH', 'HLF', 'AMKR', 'BILL', 'CATY', 'AEHR', 'AMWD', 'ITI', 'BLK', 'YUM', 'ZWS', 'MLI', 'NJR', 'PFC', 'CDMO', 'GBDC', 'MCHX', 'OSW', 'DMAA', 'ANSS', 'KAR', 'AES', 'FLXS', 'CRCW', 'NSIT', 'GENK', 'STEM', 'DAY', 'MDBH', 'STX', 'VRSN', 'HCA', 'AGO', 'ATRA', 'GGT.RT', 'GROV', 'NOV', 'CTS', 'NTHI', 'HP', 'ULBI', 'NYSE: SCS', 'MOBX', 'EVRI', 'SAIC', 'GLSI', 'MYFW', 'AKRO', 'OII', 'INVH', 'MURA', 'JELD', 'EVRG', 'PEGY', 'DGX', 'ISPO', 'UPWK', 'GAB.N', 'CART', 'SPFX', 'PPSI', 'CCTS', 'HRGN', 'HQL', 'MAIN', 'NGS', 'FREVS', 'KALU', 'VFF', 'VRNA', 'NRDE', 'TFC', 'CWAN', 'ZYME', 'OMCL', 'XLO', 'BFH', 'PLYM', 'OTRK', 'DIBS', 'LVWR', 'RLJ', 'BLFY', 'YMAB', 'GPK', 'HCC', 'LEGH', 'REFI', 'SMTC', 'RHP', 'NRDS', 'JHG', 'CGC', 'GGT', 'OPY', 'FRSH', 'PROF', 'FBRX', 'PUBM', 'PCB', 'BXMX', 'BRFH', 'ORI', 'FCFS', 'BANR', 'WW', 'UPBD', 'BOWL', 'THMG', 'RPAY', 'GME', 'GRPN', 'TEAM', 'VLDX', 'BFST', 'CTNT', 'PSEC', 'AVGO', 'PM', 'CCIF', 'PDSB', 'AWH', 'ACGL', 'ACDC', 'emyb', 'ASMB', 'TBLA', 'GIII', 'BTTR', 'SBFG', 'LOCL', 'CASH', 'DTE', 'BCC', 'SLG', 'TELA', 'ETO', 'OSIS', 'AFCG', 'MTUS', 'PLPC', 'TECH', 'LYFT', 'GDRX', 'HTLF', 'NPAC', 'ODCYX', 'SCD', 'CACI', 'STGW', 'DIOD', 'GRAL', 'xw#w6qqr', 'FFIE', 'AXTA', 'BDN', 'OCTIX', 'RMAX', 'PASG', 'DNA', 'GM', 'BJ', 'OBDC', 'BMC', 'UEC', 'ACCO', 'SOTK', 'MBCN', 'DYNR', 'PPBI', 'AX', 'KD', 'OPRX', 'FCO', 'ENVX', 'LLAP', 'AAOI', 'IROQ', 'OFIX', 'VTLE', 'YOU', 'KRO', 'AMAL', 'GEF, GEF-B', 'SAFT', 'REVG', 'AIRS', 'PINS', 'RVTY', 'NXU', 'HTCR', 'CHMI', 'CLMB', 'ARMK', 'SNAP', 'INSM', 'FHI', 'ELVN', 'GYRO', 'ARCC', 'ALXO', 'ACIW', 'FOLD', 'OVLY', 'HMST', 'NVCT', 'DLR', 'BCPC', 'SAIA', 'FWRG', 'ASGI', 'BMEZ', 'BRDG', 'PTMN', 'GVA', 'DTIL', 'EW', 'GTX', 'MAGN', 'LMAT', 'MA', 'UFCS', 'DOMA', 'BDSX', 'UMH', 'ZDGE', 'PAYC', 'ZUO', 'DK', 'GHLD', 'FWONK', 'MHO', 'RYI', 'ALKT', 'UVE', 'DV', 'NSC', 'ECAT', 'ETNB', 'AERG', 'JAZZ', 'IPSC', 'SYRS', 'NARI', 'XGN', 'PI', 'VRT', 'NICK', 'QUBT', 'CRK', 'KOS', 'AFG', 'NWPP', 'GKOS', 'OHI', 'AMED', 'LRN', 'CBNA', 'CUZ', 'PEGA', 'FCBC', 'LBPH', 'OESX', 'AAPL', 'COOK', 'NFBK', 'FSTR', '[NONE]', 'ASX:CRN', 'BMRN', 'MX', 'SLRN', 'FULT', 'AEVA', 'FINS', 'ARDS', 'DKNG', 'RDUS', 'HONE', 'OVID', 'VTYX', 'SGI', 'YUMC', 'NSTS', 'GWW', 'PCTY', 'EXFY', 'FSBC', 'TEL', 'GBR']

    for ticker in all_tickers:
        try:
            ticker_info = yf.Ticker(ticker).info
            company_long_name = ticker_info.get('longName')
            sector = ticker_info.get('sector')
            industry = ticker_info.get('industry')
            print(f'{company_long_name}|{ticker}|{sector}|{industry}')
        except Exception as e:
            if e.response.status_code == 404:
                # print(f'Resource not found error 404 for {ticker}, trying another ticker')
                continue
            else:
                error_causing_tickers.append(ticker)
        
    # print(error_causing_tickers)




    # go through each ticker and 

def main():
    # get_industry_sector_data()
    store_or_update_tables()

if __name__ == '__main__':
    main()