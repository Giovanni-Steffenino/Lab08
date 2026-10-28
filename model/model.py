from database.DAO import DAO
class Model:
    def __init__(self):
        self._solBest = []
        self._bestCustomers = 0          # ← unica riga nuova nel costruttore
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()

    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []
        self._bestCustomers = 0
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, 0)
        return self._solBest, self._bestCustomers

    def ricorsione(self, parziale, maxY, maxH, pos):
        # E - sempre: confronto con la migliore
        clienti = self.sumCustomers(parziale)
        if clienti > self._bestCustomers:
            self._bestCustomers = clienti
            self._solBest = list(parziale)
        for i in range(pos, len(self._listEvents)):
            evento = self._listEvents[i]
            parziale.append(evento)                       # B
            if self.isValid(parziale, maxY, maxH):        # C
                self.ricorsione(parziale, maxY, maxH, i + 1)
            parziale.pop()
            # D
    def sumCustomers(self, parziale):
        return sum(e.customers_affected for e in parziale)

    def sumHours(self, parziale):
        return sum((e.date_event_finished - e.date_event_began).total_seconds() / 3600
                   for e in parziale)

    def isValid(self, parziale, maxY, maxH):
        if self.sumHours(parziale) > maxH:
            return False
        if parziale[-1].date_event_began.year - parziale[0].date_event_began.year > maxY:
            return False
        return True

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc