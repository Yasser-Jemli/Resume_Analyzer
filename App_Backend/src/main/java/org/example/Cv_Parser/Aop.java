package org.example.Cv_Parser;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.stereotype.Component;

@Component
@Aspect
public class Aop {
    @Before("execution(* org.example.Cv_Parser.services.*.*(..))")
    public void logMethodEntity(JoinPoint joinpoint){
        String name=joinpoint.getSignature().getName();
        System.out.println("Methode :" + name);
    }
    @Around("execution(* org.example.Cv_Parser.services.*.*(..))")
    public Object profile(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        Object obj = pjp.proceed();
        long elapsedTime = System.currentTimeMillis() - start;
        System.out.println("Method execution time: " + elapsedTime + " milliseconds.");
        return obj;
    }
}
