.header on
.mode column
select
  count(1) Summary,
  sum(decided == 1) Yes,
  sum(decided == -1) No,
  sum(decided == 0) Unknown,
  sum(decided == 0 and predicted == 1) "Maybe Yes (predicted)",
  sum(decided == 0 and predicted == -1) "Maybe No (predicted)",
  sum(decided == 0 and predicted == 0) "Unknown and not predicted"
  from properties;
