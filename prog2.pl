%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% prog2.pl 
%% Oleksiy Omelchenko
%% Harmeet Singh Sohal
%% oomelche
%% hsohal
%% Program 2
%% CSE 112 Fall 2019 
%% This prolog program is a airline reservation system.  
%% Given a request to travel from one city to another, it 
%% prints out the flight schedule. For each leg of the trip,
%% it prints out the departure airport, airport, city name, 
%% and time.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Get the inputs, and call fly with the destination and source
main :- 
    read(A),
    read(B),
    fly(A, B).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% calculating the distance between airports using the haversine formula.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% convert minutes of an arc to degrees.
toDegrees(Deg1, Deg2, Min1, Min2, MinToDeg1, MinToDeg2) :-
    MinToDeg1 is Deg1 + (Min1 / 60),
    MinToDeg2 is Deg2 + (Min2 / 60).


%% obtain the longitudes and latitudes. 
toCoord(Src, Dest, Lat1, Lat2, Long1, Long2) :-
    airport(Src,  _,  degmin( Deg1, Min1), degmin( Deg2, Min2)),
    airport(Dest, _,  degmin( Deg3, Min3), degmin( Deg4, Min4)),
    toDegrees(Deg1, Deg2, Min1, Min2, MinToDeg1, MinToDeg2),
    toDegrees(Deg3, Deg4, Min3, Min4, MinToDeg3, MinToDeg4),
    Lat1  is MinToDeg1,       
    Lat2  is MinToDeg3, 
    Long1 is MinToDeg2,       
    Long2 is MinToDeg4.


%% converts the provided latitudes and longitudes from ToCoord and converts them to radians.
coordToRad( Src, Dest, Phi1, Phi2, DeltaPhi, DeltaLambda) :-
    toCoord(Src, Dest, Lat1, Lat2, Long1, Long2),
    Phi1 is Lat1 * (pi / 180),
    Phi2 is Lat2 * (pi / 180),
    DeltaPhi    is (pi / 180) * (Lat2  - Lat1),
    DeltaLambda is (pi / 180) * (Long2 - Long1).


%% computes the actual distance between two airports.
haversine(Src, Dest, Distance) :-
    coordToRad(Src, Dest, Phi1, Phi2, DeltaPhi, DeltaLambda),
    Angle is ((sin(DeltaPhi / 2) ** 2) + cos(Phi1) * cos(Phi2) * (sin(DeltaLambda / 2) ** 2)),
    Comp is 2 * atan2(sqrt(Angle), sqrt(1 - Angle)),
    Distance is (Comp * 3956). %% 3956 miles is the radius of the Earth


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Code that finds a flight path
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%% computes the hours and minutes from one airport to another.
travel_time(Src, Dest, Hours, Minutes) :-
    haversine(Src, Dest, Distance),
    Hours   is floor(Distance / 500),
    Minutes is round(((Distance / 500) - Hours) * 60).


%% looking for a flight path from one airport to another.
fly(Src, Dest) :-
    flight_path(Src, Dest, time(0, 0), [Src], AllCities, AllTimes),
    flatten(      AllCities, NCities),
    flatten(      AllTimes,  NTimes),
    print_flypath(NCities,   NTimes), !.


%% recursive predicate that searches for a given flight path between a source and destination airport.
flight_path(Start, Finish, time(MinH, MinM), Visited, [CurrCity | Cities], [CurrTime | Times]) :-
        Start \= Finish,
        (
        (travel_time(Start,  Finish, H, Min),
            flight(  Start,  Finish, time(DepH, DepM)),
            X = Finish, TempMinM is MinM + 30,

            (DepH > MinH; DepH == MinH, DepM > TempMinM),

            Depart = "depart",
            Arrive = "arrive",
            curr_cities(Start, X, SUpp, FUpp, City1, City2),
            CurrCity = [Depart, SUpp, City1, Arrive, FUpp, City2],

            ArrHours   is H   + DepH,
            ArrMin     is Min + DepM,

            (ArrMin > 59 -> (AddHours is floor(ArrMin / 60), CurrMin is round(((ArrMin / 60) - AddHours) * 60),
            CurrH is ArrHours + AddHours,
            CurrTime = [DepH, DepM, CurrH, CurrMin], !
            );

            CurrTime = [DepH, DepM, ArrHours, ArrMin], !
            )
        ); 
        (travel_time(Start, X, H, Min),
            flight(  Start, X, time(DepH, DepM)),
            not(member(X, Visited)),

            NewM is Min + 30,
            NewH is H   + DepH, NewH < 24,   

            (DepH > MinH; DepH == MinH, DepM > NewM),


            (NewM > 59 -> (AddHours is floor(NewM / 60), CurrMin is round(((NewM / 60) - AddHours) * 60),
            CurrH is NewH + AddHours, CurrH < 24,
            
            flight_path(X, Finish, time(CurrH, CurrMin), [X | Visited], Cities, Times), !);
            flight_path(X, Finish, time(NewH,  NewM),    [X | Visited], Cities, Times), !)),

            Depart = "depart",
            Arrive = "arrive",
            curr_cities(Start, X, SUpp, FUpp, City1, City2),
            CurrCity = [Depart, SUpp, City1, Arrive, FUpp, City2],

            ArrHours   is H   + DepH,
            ArrMin     is Min + DepM,

            (ArrMin > 59 -> (AddHours is floor(ArrMin / 60), CurrMin is round(((ArrMin / 60) - AddHours) * 60),
            CurrH is ArrHours + AddHours, CurrH < 24,
            CurrTime = [DepH, DepM, CurrH, CurrMin]
            );
            CurrTime = [DepH, DepM, ArrHours, ArrMin]
            )
    ).


%% obtain the destination and source airports and their respective acronyms to uppercase.
curr_cities(S, F, SUpp, FUpp, C1, C2) :-
    airport(S, C1, _, _),
    airport(F, C2, _, _),
    string_upper(S, SUpp),
    string_upper(F, FUpp).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Print predicate that formats the output
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%% prints out the fly path provided two given lists with time and cities.

print_flypath([], []).
print_flypath([_], [_]).

print_flypath([Dep, Airport1, City1, Arr, Airport2, City2 | RestCities], [DepHours, DepMin, ArrHours, ArrMin | RestTime]) :-    

    format("~6s ~3s ~s~26|  ~`0t~d~30|:~`0t~d~33|", [Dep, Airport1, City1, DepHours, DepMin]), nl,
    format("~6s ~3s ~s~26|  ~`0t~d~30|:~`0t~d~33|", [Arr, Airport2, City2, ArrHours, ArrMin]), nl,
    print_flypath(RestCities, RestTime), !.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Database for airport locations and departure times
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


airport( atl, 'Atlanta         ', degmin(  33,39 ), degmin(  84,25 ) ).
airport( bos, 'Boston-Logan    ', degmin(  42,22 ), degmin(  71, 2 ) ).
airport( chi, 'Chicago         ', degmin(  42, 0 ), degmin(  87,53 ) ).
airport( den, 'Denver-Stapleton', degmin(  39,45 ), degmin( 104,52 ) ).
airport( dfw, 'Dallas-Ft.Worth ', degmin(  32,54 ), degmin(  97, 2 ) ).
airport( lax, 'Los Angeles     ', degmin(  33,57 ), degmin( 118,24 ) ).
airport( mia, 'Miami           ', degmin(  25,49 ), degmin(  80,17 ) ).
airport( nyc, 'New York City   ', degmin(  40,46 ), degmin(  73,59 ) ).
airport( sea, 'Seattle-Tacoma  ', degmin(  47,27 ), degmin( 122,17 ) ).
airport( sfo, 'San Francisco   ', degmin(  37,37 ), degmin( 122,23 ) ).
airport( sjc, 'San Jose        ', degmin(  37,22 ), degmin( 121,56 ) ).

flight( bos, nyc, time( 7 , 30 ) ).
flight( dfw, den, time( 8 , 0  ) ).
flight( atl, lax, time( 8 , 30 ) ).
flight( chi, den, time( 8 , 45 ) ).
flight( mia, atl, time( 9 , 0  ) ).
flight( sfo, lax, time( 9 , 0  ) ).
flight( sea, den, time( 10, 0  ) ).
flight( nyc, chi, time( 11, 0  ) ).
flight( sea, lax, time( 11, 0  ) ).
flight( den, dfw, time( 11, 15 ) ).
flight( sjc, lax, time( 11, 15 ) ).
flight( atl, lax, time( 11, 30 ) ).
flight( atl, mia, time( 11, 30 ) ).
flight( chi, nyc, time( 12, 0  ) ).
flight( lax, atl, time( 12, 0  ) ).
flight( lax, sfo, time( 12, 0  ) ).
flight( lax, sjc, time( 12, 15 ) ).
flight( nyc, bos, time( 12, 15 ) ).
flight( bos, nyc, time( 12, 30 ) ).
flight( den, chi, time( 12, 30 ) ).
flight( dfw, den, time( 12, 30 ) ).
flight( mia, atl, time( 13, 0  ) ).
flight( sjc, lax, time( 13, 15 ) ).
flight( lax, sea, time( 13, 30 ) ).
flight( chi, den, time( 14, 0  ) ).
flight( lax, nyc, time( 14, 0  ) ).
flight( sfo, lax, time( 14, 0  ) ).
flight( atl, lax, time( 14, 30 ) ).
flight( lax, atl, time( 15, 0  ) ).
flight( nyc, chi, time( 15, 0  ) ).
flight( nyc, lax, time( 15, 0  ) ).
flight( den, dfw, time( 15, 15 ) ).
flight( lax, sjc, time( 15, 30 ) ).
flight( chi, nyc, time( 18, 0  ) ).
flight( lax, atl, time( 18, 0  ) ).
flight( lax, sfo, time( 18, 0  ) ).
flight( nyc, bos, time( 18, 0  ) ).
flight( sfo, lax, time( 18, 0  ) ).
flight( sjc, lax, time( 18, 15 ) ).
flight( atl, mia, time( 18, 30 ) ).
flight( den, chi, time( 18, 30 ) ).
flight( lax, sjc, time( 19, 30 ) ).
flight( lax, sfo, time( 20, 0  ) ).
flight( lax, sea, time( 22, 30 ) ).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% END PROGRAM
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

