{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "297a293f-fd53-43e5-86e7-bc01e5bc42ae",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Created 3 files: locations.csv, causes.csv, accidents.csv\n",
      "  accident_id accident_date accident_time  location_id  cause_id vehicle_type  \\\n",
      "0      TN0001    2022-04-13      10:01:00            6         1         Bike   \n",
      "1      TN0002    2023-01-31      13:20:00            7         2         Bike   \n",
      "2      TN0003    2023-09-24      20:16:00            1         5          Car   \n",
      "3      TN0004    2023-05-05      13:32:00            3         1         Auto   \n",
      "4      TN0005    2022-04-07      19:33:00            7         1          Car   \n",
      "\n",
      "   killed  injured  \n",
      "0       0        4  \n",
      "1       0        3  \n",
      "2       0        4  \n",
      "3       1        2  \n",
      "4       1        1  \n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import random\n",
    "from datetime import datetime, timedelta\n",
    "\n",
    "# --- 1. MASTER TABLE: locations (10 TN districts) ---\n",
    "locations = pd.DataFrame({\n",
    "    'location_id': range(1, 11),\n",
    "    'state': ['Tamil Nadu']*10,\n",
    "    'city': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli',\n",
    "             'Tirunelveli', 'Thoothukudi', 'Vellore', 'Gummidipundi', 'Kanchipuram']\n",
    "})\n",
    "locations.to_csv('locations.csv', index=False)\n",
    "\n",
    "# --- 2. MASTER TABLE: causes ---\n",
    "causes = pd.DataFrame({\n",
    "    'cause_id': [1,2,3,4,5],\n",
    "    'cause_name': ['Over-speeding', 'Drunk Driving', 'Mobile Phone Use', 'Wrong Side Driving', 'Fatigue']\n",
    "})\n",
    "causes.to_csv('causes.csv', index=False)\n",
    "\n",
    "# --- 3. FACT TABLE: accidents (500 real rows) ---\n",
    "rows = []\n",
    "start_date = datetime(2021,1,1)\n",
    "for i in range(1, 50001):\n",
    "    date = start_date + timedelta(days=random.randint(0, 1450))\n",
    "    hour = random.randint(0,23)\n",
    "    rows.append({\n",
    "        'accident_id': f'TN{i:04d}',\n",
    "        'accident_date': date.date(),\n",
    "        'accident_time': f'{hour:02d}:{random.randint(0,59):02d}:00',\n",
    "        'location_id': random.randint(1,10),\n",
    "        'cause_id': random.choices([1,2,3,4,5], weights=[55,15,10,10,10])[0],\n",
    "        'vehicle_type': random.choice(['Bike', 'Car', 'Lorry', 'Bus', 'Auto']),\n",
    "        'killed': random.choices([0,1,2], weights=[70,25,5])[0],\n",
    "        'injured': random.randint(0,4)\n",
    "    })\n",
    "\n",
    "accidents = pd.DataFrame(rows)\n",
    "accidents.to_csv('accidents.csv', index=False)\n",
    "print(\"Created 3 files: locations.csv, causes.csv, accidents.csv\")\n",
    "print(accidents.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "de713c17-4ec7-46b7-bcc7-90a7c1ddbc06",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.DataFrame'>\n",
      "RangeIndex: 50000 entries, 0 to 49999\n",
      "Data columns (total 8 columns):\n",
      " #   Column         Non-Null Count  Dtype \n",
      "---  ------         --------------  ----- \n",
      " 0   accident_id    50000 non-null  str   \n",
      " 1   accident_date  50000 non-null  object\n",
      " 2   accident_time  50000 non-null  str   \n",
      " 3   location_id    50000 non-null  int64 \n",
      " 4   cause_id       50000 non-null  int64 \n",
      " 5   vehicle_type   50000 non-null  str   \n",
      " 6   killed         50000 non-null  int64 \n",
      " 7   injured        50000 non-null  int64 \n",
      "dtypes: int64(4), object(1), str(3)\n",
      "memory usage: 3.1+ MB\n",
      "None\n",
      "       location_id      cause_id       killed      injured\n",
      "count  50000.00000  50000.000000  50000.00000  50000.00000\n",
      "mean       5.51888      2.056040      0.35378      1.99304\n",
      "std        2.87293      1.399264      0.57594      1.41264\n",
      "min        1.00000      1.000000      0.00000      0.00000\n",
      "25%        3.00000      1.000000      0.00000      1.00000\n",
      "50%        6.00000      1.000000      0.00000      2.00000\n",
      "75%        8.00000      3.000000      1.00000      3.00000\n",
      "max       10.00000      5.000000      2.00000      4.00000\n",
      "accident_id      0\n",
      "accident_date    0\n",
      "accident_time    0\n",
      "location_id      0\n",
      "cause_id         0\n",
      "vehicle_type     0\n",
      "killed           0\n",
      "injured          0\n",
      "dtype: int64\n"
     ]
    }
   ],
   "source": [
    "print(accidents.info())\n",
    "print(accidents.describe())\n",
    "print(accidents.isnull().sum())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "56f4d92c-e851-4701-a54e-4158b8d6228b",
   "metadata": {},
   "outputs": [],
   "source": [
    "accidents['accident_date'] = pd.to_datetime(accidents['accident_date'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "3518c9b7-aa6e-4477-86f6-7d5d6980f231",
   "metadata": {},
   "outputs": [],
   "source": [
    "accidents. to_csv('accidents_50k.csv', index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "dbfdd0ab-40fb-41b4-9e19-89616a42dd2c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>accident_date</th>\n",
       "      <th>location_id</th>\n",
       "      <th>cause_id</th>\n",
       "      <th>killed</th>\n",
       "      <th>injured</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>count</th>\n",
       "      <td>50000</td>\n",
       "      <td>50000.00000</td>\n",
       "      <td>50000.000000</td>\n",
       "      <td>50000.00000</td>\n",
       "      <td>50000.00000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>mean</th>\n",
       "      <td>2022-12-25 08:46:46</td>\n",
       "      <td>5.51888</td>\n",
       "      <td>2.056040</td>\n",
       "      <td>0.35378</td>\n",
       "      <td>1.99304</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>min</th>\n",
       "      <td>2021-01-01 00:00:00</td>\n",
       "      <td>1.00000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.00000</td>\n",
       "      <td>0.00000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25%</th>\n",
       "      <td>2021-12-29 00:00:00</td>\n",
       "      <td>3.00000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.00000</td>\n",
       "      <td>1.00000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50%</th>\n",
       "      <td>2022-12-24 00:00:00</td>\n",
       "      <td>6.00000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.00000</td>\n",
       "      <td>2.00000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>75%</th>\n",
       "      <td>2023-12-22 00:00:00</td>\n",
       "      <td>8.00000</td>\n",
       "      <td>3.000000</td>\n",
       "      <td>1.00000</td>\n",
       "      <td>3.00000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>max</th>\n",
       "      <td>2024-12-21 00:00:00</td>\n",
       "      <td>10.00000</td>\n",
       "      <td>5.000000</td>\n",
       "      <td>2.00000</td>\n",
       "      <td>4.00000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>std</th>\n",
       "      <td>NaN</td>\n",
       "      <td>2.87293</td>\n",
       "      <td>1.399264</td>\n",
       "      <td>0.57594</td>\n",
       "      <td>1.41264</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "             accident_date  location_id      cause_id       killed  \\\n",
       "count                50000  50000.00000  50000.000000  50000.00000   \n",
       "mean   2022-12-25 08:46:46      5.51888      2.056040      0.35378   \n",
       "min    2021-01-01 00:00:00      1.00000      1.000000      0.00000   \n",
       "25%    2021-12-29 00:00:00      3.00000      1.000000      0.00000   \n",
       "50%    2022-12-24 00:00:00      6.00000      1.000000      0.00000   \n",
       "75%    2023-12-22 00:00:00      8.00000      3.000000      1.00000   \n",
       "max    2024-12-21 00:00:00     10.00000      5.000000      2.00000   \n",
       "std                    NaN      2.87293      1.399264      0.57594   \n",
       "\n",
       "           injured  \n",
       "count  50000.00000  \n",
       "mean       1.99304  \n",
       "min        0.00000  \n",
       "25%        1.00000  \n",
       "50%        2.00000  \n",
       "75%        3.00000  \n",
       "max        4.00000  \n",
       "std        1.41264  "
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "accidents.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "16331c7d-b67c-4527-a7a3-de6000a25b74",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Final rows after cleaning: 43023\n"
     ]
    }
   ],
   "source": [
    "# Remove any impossible cases (killed=0 and injured=0 at same time - not an accident)\n",
    "accidents = accidents[~((accidents['killed']==0) & (accidents['injured']==0))]\n",
    "\n",
    "# Save final clean version\n",
    "accidents.to_csv('accidents_50k_clean.csv', index=False)\n",
    "print(f\"Final rows after cleaning: {len(accidents)}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "2705aa19-6b66-4d7d-8887-8231d401d34e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Saved! Location: C:\\Users\\lalitha\n",
      "accidents rows: 43100\n"
     ]
    }
   ],
   "source": [
    "locations.to_csv('locations.csv', index=False)\n",
    "causes.to_csv('causes.csv', index=False)\n",
    "accidents.to_csv('accidents.csv', index=False)\n",
    "\n",
    "import os\n",
    "print(f\"Saved! Location: {os.getcwd()}\")\n",
    "print(f\"accidents rows: {len(accidents)}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6df7497b-e408-4a7d-a9cf-8273f3dcd826",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.14.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
