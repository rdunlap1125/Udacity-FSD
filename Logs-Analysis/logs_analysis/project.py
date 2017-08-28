#!/bin/env python2.7

import datetime
import psycopg2


def execute_news_query(query):
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    retval = cursor.fetchall()
    db.close()
    return retval


def answer_question1():
    """Query the view that answers question 1 and print the answer"""
    query = "SELECT * FROM vw_question1"
    rows = execute_news_query(query)
    print 'Q1: What are the most popular three articles of all time?'
    for row in rows:
        print '    "{0}" -- {1} views'.format(row[0], row[1])


def answer_question2():
    """Query the view that answers question 2 and print the answer"""
    query = "SELECT * FROM vw_question2"
    rows = execute_news_query(query)
    print 'Q2: Who are the most popular article authors of all time?'
    for row in rows:
        print '    {0} -- {1} views'.format(row[0], row[1])


def answer_question3():
    """Query the view that answers question 3 and print the answer"""
    query = "SELECT * FROM vw_question3"
    rows = execute_news_query(query)
    print 'Q3: On which days did more than 1% of requests lead to errors?'
    for row in rows:
        print '    {0} -- {1:.1%} errors'.format(row[0], row[1])


def print_answers():
    print
    answer_question1()
    print
    answer_question2()
    print
    answer_question3()


print_answers()
