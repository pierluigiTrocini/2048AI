% fase di guess: per ogni answer set deve esserci al massimo una mossa disponibile
% in base agli stati ipotetici in input
% (si esclude a priori la mossa relativa allo stato corrente)
{move(X) : cell(X, _, _, _), X <> "current"} = 1.

fixed_corner(1, 1).

% CALCOLI PRELIMINARI - per atomi che serviranno nei weak constraints
% determina la cella con valore massimo per la mossa M
max_value(Max_X, Max_Y, Value) :- move(Move), cell(Move, Max_X, Max_Y, Value), Value == #max{V, X, Y : cell(Move, X, Y, V), V <> 0}.

% determinare la distanza manhattan tra max_value e fixed_corner
from_corner(X, Y, Distance) :- max_value(X, Y, _), fixed_corner(Fixed_x, Fixed_y), 
    &abs(X - Fixed_x; Dx), &abs(Y - Fixed_y; Dy), Distance = Dx + Dy.

% determinare la cella con valore massimo più vicina all'angolo
minimum_distance_max_value(X, Y, Distance) :- from_corner(X, Y, Distance), Distance == #min{Dist : from_corner(R, C, Dist)}.

% determinare, data la mossa Move, il numero di celle con valore diverso da zero
non_zero_cells(N) :- move(Move), N = #count{X, Y : cell(Move, X, Y, V), V <> 0}.

% WEAK CONSTRAINTS
% minimizzare la distanza minima tra max_value e fixed_corner
:~ minimum_distance_max_value(_, _, Distance), Distance <> 0. [(Distance*Distance)@7]

% non vorrei che, data una cella con valore V, la cella alla sua destra abbia un valore diverso da V / 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y + 1), V2 <> V / 2. [V@6, X, Y]
% non vorrei che, data una cella con valore V, la cella alla sua destra abbia un valore diverso da V
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y + 1), V2 <> V. [V@6, X, Y]

% non vorrei che, data una cella con valore V, la cella sotto di essa abbia un valore diverso da V / 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X + 1), V2 <> V / 2. [V@6, X, Y]
% non vorrei che, data una cella con valore V, la cella sotto di essa abbia un valore diverso da V
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X + 1), V2 <> V. [V@6, X, Y]

% non vorrei che, data una cella con valore V, la cella alla sua sinistra abbia un valore diverso da V * 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y - 1), V2 <> V * 2. [(V*2)@6, X, Y]
% non vorrei che, data una cella con valore V, la cella alla sua sinistra abbia un valore diverso da V
:~ move(Move), cell(Move, X, Y, V), cell(Move, X, Y2, V2), Y2 == (Y - 1), V2 <> V. [V@6, X, Y]

% non vorrei che, data una cella con valore V, la cella sopra ad essa abbia un valore diverso da V * 2
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X - 1), V2 <> V * 2. [(V*2)@6, X, Y]
% non vorrei che, data una cella con valore V, la cella sopra ad essa abbia un valore diverso da V
:~ move(Move), cell(Move, X, Y, V), cell(Move, X2, Y, V2), X2 == (X - 1), V2 <> V. [V@6, X, Y]

% merging: non vorrei che, date due celle adiacenti, dello stato "current", con valori uguali, non esista una cella
% con valore doppio sulla stessa riga (o sulla stessa colonna) nella griglia della mossa Move
merged_cell_x(X, Y, Y2, Move) :- cell("current", X, Y, V), cell("current", X, Y2, V),
    &abs(Y - Y2; Dy), Dy == 1,
    move(Move), cell(Move, X, _, V2), V2 == V * 2.

merged_cell_y(Y, X, X2, Move) :- cell("current", X, Y, V), cell("current", X2, Y, V),
    &abs(X - X2; Dx), Dx == 1,
    move(Move), cell(Move, _, Y, V2), V2 == V * 2.

:~ cell("current", X, Y, V), cell("current", X, Y2, V), V <> 0, not merged_cell_x(X, Y, Y2). [(V*2)@5, Y, Y2]
:~ cell("current", X, Y, V), cell("current", X2, Y, V), V <> 0, not merged_cell_y(X, Y, X2). [(V*2)@5, X, X2]


% minimizzare il numero di celle piene (valore diverso da 0)
:~ non_zero_cells(N). [N@4]

% LOOK-AHEAD
% Per ogni mossa, calcolo le celle (tra le attuali vuote) in cui può comparire un 2 (90%) o un 4(10%)
random_placement(Move, X, Y, 2) :- move(Move), cell(Move, X, Y, 0), Move <> "current".
random_placement(Move, X, Y, 4) :- move(Move), cell(Move, X, Y, 0), Move <> "current".

% minimizzare il numero di celle piene (data la nuova cella)
:~ non_zero_cells(N), move(Move), random_placement(Move, X, Y, 2). [9 * (N + 1)@3, X, Y, Move]
:~ non_zero_cells(N), move(Move), random_placement(Move, X, Y, 4). [(N + 1)@3, X, Y, Move]

% Data la mossa Move e la cella piazzata casualmente, minimizzare i casi in cui la griglia perde di consistenza
% (in base ai criteri specificati dai primi weak constraint)

% contare i casi in cui, data la mossa Move, la cella fixed_corner coincida con l'angolo fissato (e minimizzarli)
:~ move(Move), fixed_corner(X, Y), random_placement(Move, X, Y, 2). [9@2, X, Y, Move]
:~ move(Move), fixed_corner(X, Y), random_placement(Move, X, Y, 4). [1@2, X, Y, Move]

% contare i casi in cui, data la mossa Move e una cella piazzata casualmente, la cella sia alla sinistra di
% una cella (già piazzata) con valore più grande (paga V)
:~ move(Move), random_placement(Move, X, Y, 2), cell(Move, X, Y2, V), Y == (Y2 - 1), V > 2. [9 * V@1, X, Y, Move]
:~ move(Move), random_placement(Move, X, Y, 4), cell(Move, X, Y2, V), Y == (Y2 - 1), V > 4. [V@1, X, Y, Move]

% contare i casi in cui, data la mossa Move e una cella piazzata casualmente, la cella sia sopra a una cella
% (gia piazzata) con valore più grande (paga V)
:~ move(Move), random_placement(Move, X, Y, 2), cell(Move, X2, Y, V), X == (X2 - 1), V > 2. [9 * V@1, X, Y, Move]
:~ move(Move), random_placement(Move, X, Y, 4), cell(Move, X2, Y, V), X == (X2 - 1), V > 4. [V@1, X, Y, Move]




#show move/1.