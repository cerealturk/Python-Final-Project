# Isaac Burmingham
# Final Project
# Fireball Dataset



import csv
import sys
from collections import namedtuple,defaultdict
import os
import logging
import requests
import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests as re
import geopandas


class Fireball:

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('fireball.log','w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)

    def __init__(self):
        self.fireballdf = pd.read_csv('fireball_data.csv')
        logging.info("DataFrame created")



    def __str__(self):
        return f"Fireball dataset: {self.fireballdf.to_string()}"

    def __iter__(self):
        self._iter = 0
        return self

    def __next__(self):
        if self._iter == len(self.fireballdf):
            raise StopIteration
        datum = self.fireballdf[self._iter]
        self._iter += 1
        return datum

    def read_data(self): # just another way to read data without pandas
        with open("fireball_data.csv",'r') as infile:
            reader = csv.reader(infile, delimiter=',', skipinitialspace=True)
            data = [data for data in reader]
        data_array = np.asarray(data)

    def write_data(self,file):
        self.fireballdf.to_csv(file)

    def get_header(self):
        logging.info(self.fireballdf.head())

    def plot_mass(self):
        # is there a relationship between mass and radiated energy?
        df = self.fireballdf
        dfarray = df.values
        # mass is not a given field, so we have to calculate it
        ImpactEkt = df.values[:,9]
        v = df.values[:,4]

        ImpactE = 4.184E12*ImpactEkt #kt -> J
        vel = v*1000 #km/s -> m/s

        df['mass'] = (2*ImpactE)/(vel**2) #mass in kg

        #print(df['mass'])
        # we also have a few outliers that are skewing our data. For this plot and the velocity plot,
        # I am eliminating the data points that are not within 1.5 std to better understand the distribution. **3 std still had significant outliers
        df_adj = df[np.abs(df.mass-df.mass.mean()) <= (1.5*df.mass.std())] # dataframe within 1.5 std of mass average
        try:
            assert (df_adj.mass.max() > 1.5*df_adj.mass.std())


            df_adj = df_adj.copy()
            df_adj['mass'] = df_adj['mass'].astype('float64',copy=False)
            df_adj['Total Radiated Energy (J)'] = df_adj['Total Radiated Energy (J)'].astype('float64',copy=False)
            sns_plot = sns.lmplot(x='mass',y='Total Radiated Energy (J)',data=df_adj,truncate=True)
            plt.xlabel("Mass (kg)")
            plt.ylabel("Radiated Energy (J)")
            plt.show()
            #sns_plot.savefig("mass.png")
        except AssertionError:
            logging.debug("assertion failed, data invalid")



    def plot_map(self):
        # world map plotting fireball location to see if it is equally distributed over the Earth or
        #if there is a favorable side
        df = self.fireballdf

        df['Latitude (deg.)'].fillna('NaNs',inplace=True)
        df['Longitude (deg.)'].fillna('NaNs',inplace=True)

        lat = []
        long = []
        for i in df['Latitude (deg.)']:
            if i[-1] == 'S':
                lat.append(-float(i[:-1]))
            else:
                lat.append(float(i[:-1]))

        df['Latitude'] = lat

        for i in df['Longitude (deg.)']:
            if i[-1] == 'W':
                long.append(-float(i[:-1]))
            else:
                long.append(float(i[:-1]))
        df['Longitude'] = long

        df['ln_ImpactEnergy'] = np.log(df['Calculated Total Impact Energy (kt)'])

        world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

        fig,ax= plt.subplots(figsize=(12,8))

        world.plot(ax=ax,color='white',edgecolor='black',legend=False)

        plot = df.plot.scatter(x='Longitude',y='Latitude',label="Impact Energy (kt)",
        c=df['ln_ImpactEnergy'],s=20*df['Calculated Total Impact Energy (kt)'],cmap=plt.get_cmap("viridis"),
        alpha=0.7,colorbar=False,ax=ax,legend=True)
        plot.legend(loc=1, prop={'size': 8},markerscale=1/20)

        sm = plt.cm.ScalarMappable(cmap=plt.get_cmap('viridis'),
         norm=plt.Normalize(vmin=df['ln_ImpactEnergy'].min(), vmax=df['ln_ImpactEnergy'].max()))
        sm.set_array([])
        fig.colorbar(sm,label="Impact Energy (ln(kt))")

        plt.title('Total Impact Energy (kt)')

        plt.show()

        fig.savefig("world_map.png")

    def plot_velocity(self):
        # Is there a relationship between impact energy and velocity?
        df = self.fireballdf
        df['velocity'] = df['Velocity (km/s)']
        df_adj = df[np.abs(df.velocity-df.velocity.mean()) <= (1.5*df.velocity.std())]
        sns_plot = sns.lmplot(x='velocity',y='Calculated Total Impact Energy (kt)',data=df_adj)
        #plt.ylim(0,10)
        plt.xlabel("Total Impact Energy (kt)")
        plt.ylabel("Velocity (km/s)")
        plt.show()
        #sns_plot.savefig("velocityIE2.png")



def main():
    parser = argparse.ArgumentParser(description="Analyze NASA Fireball data")
    parser.add_argument("command", metavar='<command>', help='command to execute')
    parser.add_argument("-he",'--header',action='store_true',
    help='get the first 5 rows of the DataFrame')
    parser.add_argument("-o","--ofile",metavar='<outfile>', help='file to write to, default is standard output')
    parser.add_argument("-p","--plot",
    help="Plot the output with by either the map, velocity or mass",choices=['map','velocity','mass'])
    args = parser.parse_args()

    myData = Fireball()

    if args.ofile:
        with open(args.ofile, 'w',newline='') as outfile:
            writer = csv.writer(outfile, dialect='excel')

            if args.command == 'print':

                if args.header:
                    myData.get_header()

                if args.plot == 'map':
                    myData.plot_map()
                    logging.info('Finished')

                elif args.plot == 'velocity':
                    myData.plot_velocity()
                    logging.info('Finished')

                elif args.plot == 'mass':
                    myData.plot_mass()
                    logging.info('Finished')

                else:
                    logging.debug("No input specified")


                myData.write_data(args.ofile)


    else:
        if args.command == 'print':

            if args.header:
                myData.get_header()

            if args.plot == 'map':
                myData.plot_map()
                logging.info('Map created')

            elif args.plot == 'velocity':
                myData.plot_velocity()
                logging.info('velocity created')

            elif args.plot == 'mass':
                myData.plot_mass()
                logging.info('mass created')

            else:
                logging.debug("No input specified")

            sys.stdout.write(str(myData))



if __name__ == "__main__":
    main()
