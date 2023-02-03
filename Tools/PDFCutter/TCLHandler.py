from Tools.PDFCutter.Validater import *
from Tools.PDFCutter.DateTimeSearcher import *


class TCLHandler:
    def __init__(self):
        self.Vali = Validater()
        self.DateS = DatetimeSearcher()
        self.TCLIdentifier = ['türreparatur', "checkliste"]

    def IsThisaTclProtokoll(self, AllTokens):
        # Checks if Page is a PZB document

        AllTokens = self.Vali.lowercastTokens(AllTokens)
        if len(set(self.TCLIdentifier) - set(AllTokens)) == 0:
            return True
        return False

    def getTCLDokumentName(self, AllTokens):

        # Handels PZB Documents

        Date = self.DateS.findLatestDateTimeBouthFormats(AllTokens)
        Fahrzeugnummer = self.Vali.getShortZugNummer(AllTokens)
        if Fahrzeugnummer is None:
            Fahrzeugnummer = self.Vali.getFzNummerShort(AllTokens)
        if Date is not None and Fahrzeugnummer is not None:
            ReleaseDocName = Fahrzeugnummer + '_' + str(Date.year) + str(Date.month) + str(Date.day) + '_' + 'TCL'
        else:
            ReleaseDocName = 'TCLDokument'
        return ReleaseDocName

    def isDefinedName(self, PageName):

        # Checks if the Dokument ist a 'LVADokument' which is specified.

        PageNameParts = PageName.split('_')
        if ((len(PageNameParts) != 3 or
             not self.Vali.isZugNr(PageNameParts[0]) or
             not (len(PageNameParts[1]) <= 8 and len(PageNameParts[1]) >= 6) or
             not PageNameParts[1].isnumeric()) or
                not PageNameParts[2] == 'TCL'):
            return False
        return True

    def specifieUnpecifiedDoc(self, DestinationFiles, UnspecifiedPage):

        # Tries to returns a specified Name for the 'PZB'
        # DestinationFiles: List of al DestinationFilenNames
        # UnspecifiedPage: Name of the currently unspecified Freigabdokument.

        DefinedPage = ''
        for Page in DestinationFiles:
            if self.isDefinedName(Page):
                if DefinedPage == '':
                    DefinedPage = Page
                elif DefinedPage != Page:
                    return UnspecifiedPage
        return DefinedPage
