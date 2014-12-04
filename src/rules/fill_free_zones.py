from rules.base import Rule


class FillFreeZonesRule(Rule):
    def apply(self):
        df = self.df
        for i, row in df.iterrows():
            row._find_unknown_zones()
            potetial_zone = row.zones[row.zones['len']/2 < row.name.data]
            pass



FillFreeZonesRule()