from decimal import Decimal

def coins(M, n):
    dp = [None]*(n + 1)
    s = [None]*(n + 1);
    
    dp[0] = 0;
    s[0] = 0;

    for i in range(1, n + 1):
      dp[i] = Decimal('Infinity');
      s[i] = 0;

      for j in range(0, len(M)):
        if i >= M[j]:
          if dp[i - M[j]] + 1 < dp[i]: 
              dp[i] = dp[i - M[j]] + 1;
              s[i] = M[j];
    
    solution = []
    while(n != 0):
          print('1 moeda de ', s[n])
          solution.append(s[n])
          n = n - s[n]

    return solution

print(coins([1, 2,5,10,20,50,100,200], 2195))