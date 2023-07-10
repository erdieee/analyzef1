import logging
from typing import Any, List

import fastf1
import fastf1.plotting
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import numpy as np
from fastf1.core import Laps
from matplotlib.collections import LineCollection
from timple.timedelta import strftimedelta
import streamlit as st
from analyzef1.data_management.data_handler import DataHandler

logger = logging.getLogger(__name__)
fastf1.plotting.setup_mpl(misc_mpl_mods=False)


class Plotter:
    """
    Class responsable for creating all graphics
    """

    @staticmethod
    def plot_drivers_fastest_laps(session):
        drivers = pd.unique(session.laps["Driver"])
        list_fastest_laps = list()
        team_colors = list()
        for drv in drivers:
            drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
            list_fastest_laps.append(drvs_fastest_lap)
        fastest_laps = (
            Laps(list_fastest_laps).sort_values(by="LapTime").reset_index(drop=True)
        )
        pole_lap = fastest_laps.pick_fastest()
        fastest_laps["LapTimeDelta"] = fastest_laps["LapTime"] - pole_lap["LapTime"]

        for index, lap in fastest_laps.iterlaps():
            color = fastf1.plotting.team_color(lap["Team"])
            team_colors.append(color)
        fig, ax = plt.subplots()
        ax.barh(
            fastest_laps.index,
            fastest_laps["LapTimeDelta"],
            color=team_colors,
            edgecolor="grey",
        )
        ax.set_yticks(fastest_laps.index)
        ax.set_yticklabels(fastest_laps["Driver"])

        # show fastest at the top
        ax.invert_yaxis()

        # draw vertical lines behind the bars
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, which="major", linestyle="--", color="black", zorder=-1000)
        lap_time_string = strftimedelta(pole_lap["LapTime"], "%m:%s.%ms")

        plt.suptitle(
            f"{session.event['EventName']} {session.event.year} {session.event['Session3']}\n"
            f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})"
        )
        return fig

    @staticmethod
    def boxplot_drivers_laps(session):
        laps = DataHandler.get_drivers_laps(session)
        eventname = session.event["EventName"]
        driver_laps = []
        driver = []
        team_colors = []

        for drivers in range(len(laps)):
            laptime = pd.DataFrame(
                laps[drivers][["LapTime", "TrackStatus", "PitOutTime"]]
            )
            laptime["GreenFlag"] = laptime["TrackStatus"].str.contains("1")
            laptime["LapInPit"] = laptime["PitOutTime"].isna()
            # remove outliers
            laptime["GreenFlag"].replace(False, np.nan, inplace=True)
            laptime["LapInPit"].replace(False, np.nan, inplace=True)
            laptime["LapTimeInSeconds"] = laptime["LapTime"].dt.total_seconds()
            laptime.dropna(
                axis="index",
                subset=["LapTimeInSeconds", "GreenFlag", "LapInPit"],
                inplace=True,
            )
            laptime = laptime.reset_index()

            driver_laps.append(laptime["LapTimeInSeconds"])
            driver.append(laps[drivers]["Driver"].iloc[0])
            team_colors.append(
                fastf1.plotting.team_color(laps[drivers]["Team"].iloc[0])
            )

        fig, ax = plt.subplots()
        bplot = ax.boxplot(driver_laps, showfliers=False)
        ax.set_title(f"Racepace at {eventname}-{session.event.year}")
        ax.set_xticklabels(driver)
        ax.set_ylabel("Laptime in [s]")
        plt.xticks(fontsize=6)
        for artist, color in zip(bplot["boxes"], team_colors):
            patch = mpatches.PathPatch(artist.get_path(), color=color)
            ax.add_artist(patch)
        for median in bplot["medians"]:
            median.set(color="black", linewidth=1)

        return fig

    @staticmethod
    def racepace_laps(session):
        laps = DataHandler.get_drivers_laps(session)
        eventname = session.event["EventName"]
        driver_name = []
        length_race = []
        race_numbers = []
        team_colors = []
        for drivers in range(len(laps)):
            laptime = pd.DataFrame(
                laps[drivers].loc[
                    :,
                    [
                        "LapTime",
                        "LapNumber",
                        "Team",
                        "PitOutTime",
                        "TrackStatus",
                        "Driver",
                    ],
                ]
            )
            laptime["LapTimeInSeconds"] = laptime["LapTime"].dt.total_seconds()
            laptime["PitOutTimeInSeconds"] = laptime["PitOutTime"].dt.total_seconds()
            laptime = laptime.reset_index()
            laptime["LapTimeMean"] = (
                laptime["LapTimeInSeconds"]
                .rolling(25, center=True, min_periods=1)
                .mean()
            )
            length_race.append(laptime.loc[:, "LapTimeMean"])
            race_numbers.append(laptime["LapNumber"])
            driver_name.append(laptime["Driver"].iloc[0])
            team_colors.append(fastf1.plotting.team_color(laptime["Team"].iloc[0]))

        fig, ax = plt.subplots()
        x = []
        y = []
        for i in range(len(length_race)):
            x.append(np.array(race_numbers)[i])
            y.append(np.array(length_race)[i])
        for i in range(len(x)):
            ax.plot(x[i], y[i], color=team_colors[i])
        ax.set_title(f"Racepace at {eventname}")
        ax.set_facecolor("lightgrey")
        ax.legend(
            driver_name,
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fancybox=True,
            shadow=True,
            facecolor="lightgrey",
        )

        return fig

    @staticmethod
    def colormap_map_speed(session, driver: Any):
        colormap = mpl.cm.plasma
        event_name = session.event["EventName"]
        lap = session.laps.pick_driver(driver).pick_fastest()
        # Get telemetry data
        x = lap.telemetry["X"]  # values for x-axis
        y = lap.telemetry["Y"]  # values for y-axis
        color = lap.telemetry["Speed"]  # value to base color gradient on
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
        fig.suptitle(
            f"{event_name} {session.event.year} - {driver} - Speed", size=24, y=0.97
        )
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        ax.axis("off")
        # Create background track line
        ax.plot(
            lap.telemetry["X"],
            lap.telemetry["Y"],
            color="black",
            linestyle="-",
            linewidth=16,
            zorder=0,
        )
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(color.min(), color.max())
        lc = LineCollection(
            segments, cmap=colormap, norm=norm, linestyle="-", linewidth=5
        )
        # Set the values used for colormapping
        lc.set_array(color)
        # Merge all line segments together
        line = ax.add_collection(lc)
        # Create a color bar as a legend.
        cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
        normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
        legend = mpl.colorbar.ColorbarBase(
            cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal"
        )

        return fig

    @staticmethod
    def colormap_map_gear_shifts(session, driver: Any):
        event_name = session.event["EventName"]
        lap = session.laps.pick_driver(driver).pick_fastest()
        tel = lap.get_telemetry()

        x = np.array(tel["X"].values)
        y = np.array(tel["Y"].values)
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        gear = tel["nGear"].to_numpy().astype(float)

        colormap = mpl.cm.get_cmap("Paired")

        fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
        fig.suptitle(
            f"{event_name} {session.event.year} - {driver} - Gear Shift",
            size=24,
            y=0.97,
        )
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        ax.axis("off")

        # Create background track line
        ax.plot(
            tel["X"], tel["Y"], color="black", linestyle="-", linewidth=12, zorder=0
        )
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(1, colormap.N + 1)
        lc = LineCollection(
            segments, cmap=colormap, norm=norm, linestyle="-", linewidth=5
        )
        lc.set_array(gear)
        line = ax.add_collection(lc)
        cbar = fig.colorbar(
            lc, label="Gear", boundaries=np.arange(1, 10), location="bottom", shrink=0.6
        )
        cbar.set_ticks(np.arange(1.5, 9.5))
        cbar.set_ticklabels(np.arange(1, 9))
        return fig

    @staticmethod
    def driver_position_during_race(session):
        fig, ax = plt.subplots(figsize=(8.0, 4.9))
        for drv in session.drivers:
            drv_laps = session.laps.pick_driver(drv)

            abb = drv_laps["Driver"].iloc[0]
            color = fastf1.plotting.driver_color(abb)

            ax.plot(drv_laps["LapNumber"], drv_laps["Position"], label=abb, color=color)
        ax.set_ylim([20.5, 0.5])
        ax.set_yticks([1, 5, 10, 15, 20])
        ax.set_xlabel("Lap")
        ax.set_ylabel("Position")
        ax.legend(bbox_to_anchor=(1.0, 1.02))
        plt.tight_layout()
        return fig

    @staticmethod
    def compare_2_drv_lap(session, drivers: List, lapnumber: int):
        laps = session.laps
        laps_driver_1 = laps.pick_driver(drivers[0])
        laps_driver_2 = laps.pick_driver(drivers[1])
        lap_telemetry_driver_1 = (
            laps_driver_1.loc[laps_driver_1["LapNumber"] == lapnumber + 1]
            .get_car_data()
            .add_distance()
        )
        lap_telemetry_driver_2 = (
            laps_driver_2.loc[laps_driver_2["LapNumber"] == lapnumber + 1]
            .get_car_data()
            .add_distance()
        )

        plt.rcParams["figure.figsize"] = [15, 15]
        fig, ax = plt.subplots(4)
        fig.suptitle(
            f"Lap {lapnumber} Telemetry Comparison between {drivers[0]} and {drivers[1]}",
            fontsize=16,
        )

        telemetry = [lap_telemetry_driver_1, lap_telemetry_driver_2]
        types = ["Speed", "Throttle", "Brake", "DRS"]

        for i, desc in enumerate(types):
            for j, tel in enumerate(telemetry):
                ax[i].plot(tel["Distance"], tel[desc], label=drivers[j])

        ax[0].legend()
        ax[0].set(ylabel="Speed [km/h]")
        ax[1].set(ylabel="Throttle in %")
        ax[2].set(ylabel="Brakes in %")
        ax[3].set(ylabel="DRS")
        ax[3].set(xlabel="Distance [m]")
        # Set Ticks Distance to 500m, grid visible
        for i in range(len(ax)):
            ax[i].set(xticks=np.arange(0, max(lap_telemetry_driver_1["Distance"]), 500))
            ax[i].grid(visible=True)
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for a in ax.flat:
            a.label_outer()

        return fig

    @staticmethod
    def leadboard_driver_line_plot(data, year):
        data.drop(columns="Total", inplace=True)
        data.fillna(value=0, inplace=True)
        data.columns = [int(i + 1) for i in range(len(data.columns))]
        for i in range(1, len(data.columns)):
            data.iloc[:, i] = data.iloc[:, i - 1] + data.iloc[:, i]
        fig, ax = plt.subplots(figsize=(12, 8))
        for i, driver in enumerate(data.index):
            try:
                color = fastf1.plotting.driver_color(driver)
            except Exception as e:
                logger.warning(e)
            ax.plot(data.columns, data.iloc[i], label=driver, color=color)
        ax.set_xlabel("Round")
        ax.set_ylabel("Points")
        ax.legend(bbox_to_anchor=(1.0, 1.02))
        plt.title(f"Driver standings {year}")
        plt.grid()
        plt.tight_layout()
        return fig

    @staticmethod
    def leadboard_constructor_line_plot(data, year):
        fig, ax = plt.subplots(figsize=(8.0, 4.9))
        for i, constructor in enumerate(data.index):
            color = fastf1.plotting.team_color(constructor)
            ax.plot(data.columns, data.iloc[i], label=constructor, color=color)
        ax.set_xlabel("Round")
        ax.set_ylabel("Points")
        ax.legend(bbox_to_anchor=(1.0, 1.02))
        plt.title(f"Constructor standings {year}")
        plt.grid()
        plt.tight_layout()
        return fig

    @staticmethod
    def leadboard_driver_heatmap_plot(results):
        fig = px.imshow(
            results,
            text_auto=True,
            aspect="auto",  # Automatically adjust the aspect ratio
            color_continuous_scale=[
                [0, "rgb(198, 219, 239)"],  # Blue scale
                [0.25, "rgb(107, 174, 214)"],
                [0.5, "rgb(33,  113, 181)"],
                [0.75, "rgb(8,   81,  156)"],
                [1, "rgb(8,   48,  107)"],
            ],
            labels={
                "x": "Race",
                "y": "Driver",
                "color": "Points",
            },  # Change hover texts
        )
        fig.update_xaxes(title_text="")  # Remove axis titles
        fig.update_yaxes(title_text="")
        fig.update_yaxes(tickmode="linear")  # Show all ticks, i.e. driver names
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor="LightGrey",
            showline=False,
            tickson="boundaries",
        )  # Show horizontal grid only
        fig.update_xaxes(showgrid=False, showline=False)  # And remove vertical grid
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")  # White background
        fig.update_layout(coloraxis_showscale=False)  # Remove legend
        fig.update_layout(xaxis=dict(side="top"))  # x-axis on top
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins
        return fig

    @staticmethod
    def tyre_strategy(session, year, event):
        laps = session.laps
        drivers = [
            session.get_driver(driver)["Abbreviation"] for driver in session.drivers
        ]
        stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
        stints = stints.groupby(["Driver", "Stint", "Compound"])
        stints = stints.count().reset_index()
        stints = stints.rename(columns={"LapNumber": "StintLength"})
        fig, ax = plt.subplots(figsize=(5, 10))

        for driver in drivers:
            driver_stints = stints.loc[stints["Driver"] == driver]

            previous_stint_end = 0
            for idx, row in driver_stints.iterrows():
                # each row contains the compound name and stint length
                # we can use these information to draw horizontal bars
                plt.barh(
                    y=driver,
                    width=row["StintLength"],
                    left=previous_stint_end,
                    color=fastf1.plotting.COMPOUND_COLORS[row["Compound"]],
                    edgecolor="black",
                    fill=True,
                )

                previous_stint_end += row["StintLength"]

        plt.title(f"{year} {event} Tyre Strategies")
        plt.xlabel("Lap Number")
        plt.grid(False)
        # invert the y-axis so drivers that finish higher are closer to the top
        ax.invert_yaxis()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        plt.tight_layout()
        return fig
