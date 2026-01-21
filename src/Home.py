import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from millify import prettify

# Reference: Columns in our dataframe (migrantdf.columns):
# ['Unnamed: 0', 'Main ID', 'Incident ID', 'Incident Type',
#    'Region of Incident', 'Incident year', 'Reported Month',
#    'Number of Dead', 'Minimum Estimated Number of Missing',
#    'Total Number of Dead and Missing', 'Number of Survivors',
#    'Number of Females', 'Number of Males', 'Number of Children',
#    'Country of Origin', 'Region of Origin', 'Cause of Death',
#    'Migration route', 'Location of death', 'Information Source',
#    'Coordinates', 'UNSD Geographical Grouping', 'X', 'Y']

# Import the data
data_url = "data/Missing_Migrants_Global_Figures_filtered.csv"

# Prepare the Data


@st.cache
def get_data():
    url = data_url
    return pd.read_csv(url)


df = get_data()
df = df.rename(columns={"X": "lon", "Y": "lat"})
migrantdf = df


def get_df():
    '''Exports the full dataframe for use in other pages'''
    return df


# 0. Section for  Sidebar filters   *      *       *      *      *       *      *      *       *      *      *       *
# 0.1 Migration Route filter
st.sidebar.write("Data Filters")
route_input = st.sidebar.multiselect(
    'Migration Route', df['Migration route'].unique().tolist())
if len(route_input) > 0:
    migrantdf = migrantdf[migrantdf['Migration route'].isin(route_input)]
    show_route_death = True

# 0.2 Cause of death filter
cause_of_death_input = st.sidebar.multiselect(
    'Cause of Death', df['Cause of Death'].unique().tolist())
if len(cause_of_death_input) > 0:
    migrantdf = migrantdf[migrantdf['Cause of Death'].isin(
        cause_of_death_input)]

year_input = st.sidebar.multiselect('Year',
                                    df['Incident year'].unique().tolist())
if len(year_input) > 0:
    year_input.sort()
    migrantdf = migrantdf[migrantdf['Incident year'].isin(
        year_input)]

# 1.0 Introduction in Main Body  *      *       *      *      *       *      *      *       *      *      *       *
# 1.1 title and subtitle
st.title("Visualizing Deaths of Migrants at Borders")
st.markdown("*This work began as a course project at the University of Helsinki alongside [Sebastian Rodriguez-Beltran](https://www.linkedin.com/in/sebastian-rodriguez-beltran-1e/?originalSubdomain=fi)*")
st.markdown("This project seeks to document and honor the lives lost during migration. We rely on data from the [Missing Migrants Project](https://missingmigrants.iom.int/), a comprehensive database tracking migrant deaths and disappearances worldwide since 2014. The dataset currently spans through 2026 and includes over 21,000 documented incidents across the globe. Each point on our map represents one or more individuals who died while migrating, with available details about location, cause of death, time period, and circumstances.")
st.markdown("The interactive visualization below allows you to explore how these tragedies vary by geographic region, migration route, cause of death, and time period. Use the filters in the left sidebar to focus on specific years, routes, or causes of death.")
st.markdown("**A note on the data:** These figures represent real people—individuals who left their homes seeking safety, opportunity, or reunion with loved ones, and who lost their lives in the process. The numbers presented here are minimum estimates; many deaths go unreported or undocumented. Behind each data point is a person with a story, a family grieving their loss, and a community forever changed.")
st.markdown("While some migration routes and tragedies receive media attention, this data reveals that migrant deaths occur daily across numerous routes worldwide. Many dangerous journeys remain largely invisible to the public. This visualization aims to bring awareness to the scale and ongoing nature of this humanitarian crisis.")
st.markdown("Explore the visualization below by zooming into the map or using the filters in the left sidebar. First, let's examine some global statistics.")
# 1.2 Global Statistics
# st.markdown(str(year_input), str(len(year_input)))
if len(year_input) == 1:
    year_text = " in " + str(year_input[0])
elif len(year_input) == 2:
    year_text = " in " + str(year_input[0]) + ' and ' + str(year_input[1])
elif len(year_input) > 2:
    year_text = " in " + str(year_input[0])
    for year in year_input[1:-1]:
        year_text += ', ' + str(year)
    year_text += ', and ' + str(year_input[-1])
else:
    year_text = ''

if len(year_input) > 0:
    statsdf = df[df['Incident year'].isin(
        year_input)]
else:
    statsdf = df
df_cause_of_death = statsdf.groupby('Cause of Death Abbreviation')['Cause of Death Abbreviation', 'Total Number of Dead and Missing'].sum(
).sort_values('Total Number of Dead and Missing', ascending=False).reset_index()
df_cause_of_death['Total Number of Dead and Missing'] = df_cause_of_death['Total Number of Dead and Missing'].apply(
    lambda x: prettify(x))

st.subheader(f'Global Statistics' + str(year_text))
st.markdown(f'Most common causes of death')
st.dataframe(df_cause_of_death, height=200)

col2, col3 = st.columns(2)
with col2:
    st.metric(f'Total number of Recorded Dead and Missing',
              prettify(statsdf['Total Number of Dead and Missing'].sum()))
with col3:
    st.metric(f'Total Number of Recorded Survivors',
              prettify(statsdf['Number of Survivors'].sum()))

# 1.3 Display the map
fig = go.Figure(data=go.Scattergeo(
    lon=migrantdf['lon'],
    lat=migrantdf['lat'],
    text=migrantdf['Cause of Death Abbreviation'],
    #hoverlabel=migrantdf['Migration route'],
    hoverinfo=['text'],
    mode='markers',
    marker_color='rgb(210,30,0)',
    marker=dict(
        colorscale='Reds'
    )
))

fig.update_layout(
    title='Locations of the Reports',
    autosize=False,
    # width=750,
    # height=400,
    geo=dict(
        scope='world',
        showcountries=True,
        showocean=True,
        landcolor="#f2f2f0",
        oceancolor="#cad2d3",
        showcoastlines=False,
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
)

# changing column names for the hovering capability
plotdf = migrantdf[['lat', 'lon']]
plotdf['Migration Route'] = migrantdf['Migration route']
plotdf['Cause of Death'] = migrantdf['Cause of Death Abbreviation']
plotdf['Year'] = migrantdf['Incident year']
plotdf['People Dead/Missing'] = migrantdf['Total Number of Dead and Missing']

plot = px.scatter_geo(plotdf, lat='lat', lon='lon',
                      hover_name='Migration Route',
                      hover_data={'Cause of Death': True,
                                  'People Dead/Missing': True,
                                  'Year': True,
                                  'lon': False,
                                  'lat': False
                                  },
                      color_discrete_sequence=['red']
                      )

plot.update_layout(
    title='Locations of the Reports',
    autosize=False,
    # width=750,
    # height=400,
    geo=dict(
        scope='world',
        showcountries=True,
        showocean=True,
        landcolor="#f2f2f0",
        oceancolor="#cad2d3",
        showcoastlines=False,
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
)

st.header("Explore the World Map")
st.markdown("When you hover over the graph with your mouse, you'll see additional data appear. Each dot on the graph marks a single incident, and the tooltip for that dot gives data on: (1) Cause of Death, (2) How many total people died or went missing for the incident, and (3) Which year the incident occured in.")
st.markdown("The map can be made full-screen. When you hover over the map, a menu should appear above it. The right-most arrows, when selected, will make the map full screen.")
st.plotly_chart(plot)

#  1.4 Explore tabular data
st.header("Explore the Tabular Data")
total_no_deaths = prettify(df['Total Number of Dead and Missing'].sum())
total_med_deaths = prettify(df[df['Migration route'].isin(
    ['Central Mediterranean', 'Western Mediterranean', 'Eastern Mediterranean'])]['Total Number of Dead and Missing'].sum())
total_drown_deaths = prettify(df[df['Cause of Death'].isin(
    ['Drowning'])]['Total Number of Dead and Missing'].sum())

st.markdown(
    "The data used in this project is collected and shared by the [Missing Migrants Project](https://missingmigrants.iom.int/). Each incident tracked by the project involves a migrant, refugee, or asylum-seeker who has died or gone missing while migrating across a border.")
st.markdown(" There have been over " + total_no_deaths + " recorded deaths since 2014. The **most deadly region is the Mediterranean**, where at least " + total_med_deaths + " deaths have been recorded. The most common **cause of death** across the world is drowning, with at least " +
            total_drown_deaths + " recorded deaths.")
st.markdown("All of these estimates are undercounts, as the project does not include counts of deaths or disappearances of migrants who have been established in a home, such as a refugee camp, or the deaths of persons who die within their country of origin despite beginning their journey.")
st.markdown('From the Missing Migrant Project:\n\n *"Missing Migrants Project data include the deaths of migrants who die in transportation accidents, shipwrecks, violent attacks, or due to medical complications during their journeys. It also includes the number of corpses found at border crossings that are categorized as the bodies of migrants, on the basis of belongings and/or the characteristics of the death. For instance, a death of an unidentified person might be included if the decedent is found without any identifying documentation in an area known to be on a migration route.  Deaths during migration may also be identified based on the cause of death, especially if is related to trafficking, smuggling, or means of travel such as on top of a train, in the back of a cargo truck, as a stowaway on a plane, in unseaworthy boats, or crossing a border fence.  While the location and cause of death can provide strong evidence that an unidentified decedent should be included in Missing Migrants Project data, this should always be evaluated in conjunction with migration history and trends."*')
st.markdown(
    'Explore the tabular data yourself using the filters in the left side menu.')
st.dataframe(migrantdf)
