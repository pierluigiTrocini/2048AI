% fase di guess: per ogni answer set deve esserci al massimo una mossa disponibile
% in base agli stati ipotetici in input
% (si esclude a priori la mossa relativa allo stato corrente)
{move(X) : cell(X, _, _, _), X <> "current"} = 1.

% Minimizzare il numero di celle non vuote
non_vuote(N) :- move(Move), N = #count{X, Y : cell(Move, X, Y, Value), Value <> 0}.
:~ non_vuote(N). [N@1]