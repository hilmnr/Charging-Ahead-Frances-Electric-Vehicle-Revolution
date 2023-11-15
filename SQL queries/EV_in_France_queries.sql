-- Total number of EVs sold and total number of charging points by country, regardless of year ---
SELECT 
c.region AS country,
SUM(s.value) AS total_ev_sales,
SUM(c.value) AS total_charging_points
FROM charging_points_world c
JOIN sales_ev_world s 
ON c.region = s.region
GROUP BY c.region
ORDER BY total_ev_sales DESC;

-- Compares the number of EV sales and charging points year over year for a specific country.--
SELECT 
s.region as country,
s.year,
s.value AS ev_sales,
c.value AS charging_points
FROM sales_ev_world s
JOIN charging_points_world c 
ON s.region = c.region AND s.year = c.year
WHERE s.region = 'France' 
ORDER BY s.year;

-- Top 5 vehicle models in France (based on units sold, years 2019-2022).--
SELECT modele as vehicle_model,
SUM(ventes) AS units_sold,
'2019-2022' AS data_range
FROM sales_top_selling_models
GROUP BY modele
ORDER BY units_sold DESC
LIMIT 5;

-- Total number of charging points per type (slow/fast charging) and per country.--
SELECT 
region AS country,
CASE
WHEN LOWER(TRIM(powertrain)) = 'publicly available fast' THEN 'Fast Charging'
WHEN LOWER(TRIM(powertrain)) = 'publicly available slow' THEN 'Slow Charging'
ELSE TRIM(powertrain)
END AS power_train_type,
SUM(value) AS total_charging_points
FROM charging_points_world
GROUP BY 
country, 
power_train_type
ORDER BY 
country, power_train_type;

-- Total charging points in France by type (public/private/corporate) for years 2015-2023--
SELECT points_de_charge_par_type, SUM(valeur) as total,
'2015-2021' AS data_range
FROM EV_in_France.charging_points_per_type
GROUP BY points_de_charge_par_type;
 
-- Charging Points Density by Department -- in descending order, to identify which departments are most densely equipped with public charging points.
SELECT 
departement,
code_departement,
nombre_pc_au_public_100_000_habitants AS charging_points_per_100k
FROM charging_points_per_departement
ORDER BY 
nombre_pc_au_public_100_000_habitants DESC;

-- Total EV Registrations per Year--
SELECT annee AS year,
SUM(valeur) AS total_registrations
FROM immatriculations_voitures_ev
GROUP BY annee
ORDER BY annee;

-- Monthly EV Registrations for a Specific Year --
SELECT mois AS month,
valeur AS monthly_registrations
FROM immatriculations_voitures_ev
WHERE annee = 2020 -- Replace with the year of interest
ORDER BY mois;

-- Total Registrations of EVs by Energy Type (2011-2021) --
SELECT type_energie AS energy_type,
SUM(valeur) * 1000 AS total_registrations
FROM EV_in_France.`immatriculations _voitures_ev_par_type`
GROUP BY energy_type
ORDER BY total_registrations DESC;

-- Yearly Trend for the 'Electricite' Type of Energy (2011-2021) --
SELECT annee AS year,
SUM(valeur) * 1000 AS total_registrations
FROM EV_in_France.`immatriculations _voitures_ev_par_type`
WHERE type_energie LIKE '%Electricite%'
GROUP BY year
ORDER BY year;

-- Monthly EV Registrations Over a Year --
SELECT mois, SUM(valeur) as total_registrations
FROM immatriculations_voitures_ev
WHERE annee = '2021'
GROUP BY mois
ORDER BY mois;

-- Annual EV Registrations Trend --
SELECT annee, SUM(valeur) as total_registrations
FROM immatriculations_voitures_ev
GROUP BY annee
ORDER BY annee;

-- Total Budget Allocation Per Initiative 2018-2023 --
SELECT gov_initiative, SUM(valeur) AS total_budget
FROM gov_ev_initiatives_budget
GROUP BY gov_initiative
ORDER BY total_budget DESC;

-- Yearly Budget Allocation for EV Initiatives 2018-2023--
SELECT annee, SUM(valeur) AS annual_budget
FROM gov_ev_initiatives_budget
GROUP BY annee
ORDER BY annee;