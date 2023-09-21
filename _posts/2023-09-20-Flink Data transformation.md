---
layout: post
title: "Flink Data Transformation"
date: 2023-09-20 
description: "flink常用的数据转换的中间操作"

# tag: Flink

# Flink Data Transformation

# 1.前言

![img](/images/YbZnoM.jpg)

Flink 应用程序结构就是如上图所示：

1、Source: 数据源，Flink 在流处理和批处理上的 source 大概有 4 类：基于本地集合的 source、基于文件的 source、基于网络套接字的 source、自定义的 source。自定义的 source 常见的有 Apache kafka、Amazon Kinesis Streams、RabbitMQ、Twitter Streaming API、Apache NiFi 等，当然你也可以定义自己的 source。

2、Transformation：数据转换的各种操作，有 Map / FlatMap / Filter / KeyBy / Reduce / Fold / Aggregations / Window / WindowAll / Union / Window join / Split / Select / Project 等，操作很多，可以将数据转换计算成你想要的数据。

3、Sink：接收器，Flink 将转换计算后的数据发送的地点 ，你可能需要存储下来，Flink 常见的 Sink 大概有如下几类：写入文件、打印出来、写入 socket 、自定义的 sink 。自定义的 sink 常见的有 Apache kafka、RabbitMQ、MySQL、ElasticSearch、Apache Cassandra、Hadoop FileSystem 等，同理你也可以定义自己的 Sink。

# 2.Transformtion

## 2.1 Map

输入是一个数据流，输出的也是一个数据流

```java
data.map(new MapFunction<String, String>() {
    @Override
    public String map(String value) throws Exception {
        return value.toUpperCase(Locale.ROOT);
    }
}).print();

输入：
hello world!
hello liu!
输出:
11> HELLO WORLD!
1> HELLO LIU!
```

## 2.2 Flat Map

采用一条记录并输出零个，一个或多个记录。

```java
data.flatMap(new FlatMapFunction<String, String>() {
    @Override
    public void flatMap(String value, Collector<String> out) throws Exception 	  {
        String[] strs = value.split(" ");
        for (String str : strs) {
            out.collect(str);
        }
    }
}).print();

输入：
hello world!
hello liu!
输出：
12> hello
12> world!
2> hello
2> liu!
```

## 2.3 Filter

过滤

## 2.4 Keyby

KeyBy 在逻辑上是基于 key 对流进行分区。在内部，它使用 hash 函数对流进行分区。它返回 KeyedDataStream 数据流。

```java
SingleOutputStreamOperator<Tuple2<String, Integer>> wordAndOne = data.flatMap(new FlatMapFunction<String, Tuple2<String, Integer>>() {
    @Override
    public void flatMap(String value, Collector<Tuple2<String, Integer>> out) throws Exception {
        String[] words = value.split(" ");
        for (String word : words) {
            Tuple2<String, Integer> wordTuple = Tuple2.of(word, 1);
            out.collect(wordTuple);
        }
    }
});
KeyedStream<Tuple2<String, Integer>, String> wordAndOneKs = wordAndOne.keyBy(new KeySelector<Tuple2<String, Integer>, String>() {
    @Override
    public String getKey(Tuple2<String, Integer> value) throws Exception {
        return value.f0;
    }
});
// 1 表示位置
SingleOutputStreamOperator<Tuple2<String, Integer>> sum = wordAndOneKs.sum(1);
sum.print();

输入：
hello world!
hello liu!
hello liu!
输出：
10> (liu!,1)
5> (hello,1)
10> (liu!,2)
5> (hello,2)
5> (hello,3)
11> (world!,1)
```

## 2.5 Reduce

Reduce 返回单个的结果值，并且 reduce 操作每处理一个元素总是创建一个新值。常用的方法有 average, sum, min, max, count，使用 reduce 方法都可实现。

```java
wordAndOneKs.reduce(new ReduceFunction<Tuple2<String, Integer>>() {
    @Override
    public Tuple2<String, Integer> reduce(Tuple2<String, Integer> value1, Tuple2<String, Integer> value2) throws Exception {
    	return Tuple2.of(value1.f0, value1.f1 + value2.f1);
    }
});
输入：
hello world!
hello liu!
hello liu!
输出：
10> (liu!,1)
5> (hello,1)
5> (hello,2)
11> (world!,1)
10> (liu!,2)
5> (hello,3)
```

上面先将数据流进行 keyby 操作，因为执行 reduce 操作只能是 KeyedStream，然后将单词做了一个求累加的操作。

## 2.6 Aggregations

DataStream API 支持各种聚合，例如 min，max，sum 等。 这些函数可以应用于 KeyedStream 以获得 Aggregations 聚合。

max返回最大值、maxBy 把最大值对应的元素全部返回

```java

	import org.apache.flink.api.java.functions.KeySelector;
	import org.apache.flink.api.java.tuple.Tuple3;
	import org.apache.flink.streaming.api.datastream.DataStreamSource;
	import org.apache.flink.streaming.api.datastream.KeyedStream;
	import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
	
	import java.util.ArrayList;
	import java.util.List;
	
	/**
	 * @Title: TSource
	 * @Description: TSource
	 * @Author: 
	 * @Date: 2021/1/13
	 */
	public class TSource {
	
	    public static void main(String[] args) throws Exception {
	
	        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
	
	        List list = new ArrayList<Tuple3<Integer, Integer, String>>();
	        list.add(new Tuple3<>(0, 1, "a"));
	        list.add(new Tuple3<>(0, 3, "b"));
	        list.add(new Tuple3<>(0, 2, "c"));
	        list.add(new Tuple3<>(0, 4, "d"));
	        list.add(new Tuple3<>(1, 5, "a"));
	        list.add(new Tuple3<>(1, 2, "b"));
	        list.add(new Tuple3<>(1, 7, "c"));
	
	        DataStreamSource<Tuple3<Integer, Integer, String>> stringDataStreamSource = env.fromCollection(list);
	
	        KeyedStream<Tuple3<Integer, Integer, String>, Integer> result = stringDataStreamSource
	                .keyBy(new KeySelector<Tuple3<Integer, Integer, String>, Integer>() {
	                           @Override
	                           public Integer getKey(Tuple3<Integer, Integer, String> value) throws Exception {
	                               return value.f0;
	                           }
	                       }
	                );
	
	        result.max(1).print("最大值");
	        result.maxBy(1).print("元素");
	
	        env.execute("测试");
	    }
	}

原数据：

原数据:3> (0,1,a)
原数据:3> (0,3,b)
原数据:3> (0,2,c)
原数据:3> (0,4,d)
原数据:3> (1,5,a)
原数据:3> (1,2,b)
原数据:3> (1,7,c)


返回结果:
最大值:3> (0,1,a)
最大值:3> (0,3,a)
最大值:3> (0,3,a)
最大值:3> (0,4,a)
最大值:3> (1,5,a)
最大值:3> (1,5,a)
最大值:3> (1,7,a)

元素:3> (0,1,a)
元素:3> (0,3,b)
元素:3> (0,3,b)
元素:3> (0,4,d)
元素:3> (1,5,a)
元素:3> (1,5,a)
元素:3> (1,7,c)
```

差在精度上

- max: 不会关心指定的聚合字段和用来比较的字段外其他字段的正确性,3个字段,以第一个为key,对第2个比较。这个函数认为用户只想知道key字段和该key上的最大数值,所以第3个字段没必要更新了。比如 (0, 1, “a”),(0, 3, “b”), (0, 2, “c”)。既然是以第一个字段为key,求第2个字段的最大值,那么只会记录,(0,1,“a”）,(0,3,a),(0,3,a)，(0,4,a),节省了空间。
- maxBy: 认为使用者关心的不仅仅是对应的key和该key的最大数值,还有其他字段,返回的整条数据都是精确的,相对上条,会返回对应最大值所在的整个元素。