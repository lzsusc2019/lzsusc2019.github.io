---
layout: post
title: "Flink Read And Write"
date: 2023-09-20 
description: "flink读取与写入"

# tag: Flink

# Flink Read And Write

# 1.About Mysql

## 1.1 Prepare 

**Dependency**

```xml
        <dependency>
            <groupId>org.apache.flink</groupId>
            <artifactId>flink-jdbc_2.12</artifactId>
            <version>1.10.1</version>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.29</version>
        </dependency>
```

**Table**

```sql
CREATE TABLE `user_order_count` (
  `user_id` varchar(25) COLLATE utf8mb3_bin NOT NULL,
  `count` int DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

insert into user_order_count values ('16935394', 6), ('16374609', 4), ('16570065', 4), ('4611433', 3), ('17308713', 3);
```

## 1.2 Read Data From MySQL

```java
    public static void main(String[] args) throws Exception {

        // ToDo 0.env
        ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        // ToDo 1.source
        DataSet<Row> dataInput = env.createInput(JDBCInputFormat.buildJDBCInputFormat()
            // 配置数据库连接信息
            .setDrivername("com.mysql.cj.jdbc.Driver")  // JDBC驱动名
            // com.mysql.jdbc.Driver：是 mysql-connector-java 5 中的
            // com.mysql.cj.jdbc.Driver：是 mysql-connector-java 6及以上 中的
            .setDBUrl("jdbc:mysql://localhost:3306/test?serverTimezone=GMT%2B8&useSSL=false")  // 数据库URL
            // jdbc:mysql://主机名:端口号/数据库名
            // serverTimezone=GMT%2B8：指定时区，设置为北京时间东八区
            // useSSL=false：MySQL 8.0以上版本 不需要建立SSL连接，需要显示关闭
            .setUsername("root")  // 用户名
            .setPassword("root")  // 登录密码
            .setQuery("select user_id, count from user_order_count")  // 需要执行的SQL语句
            .setRowTypeInfo(new RowTypeInfo(  // 设置查询的列的类型
                BasicTypeInfo.STRING_TYPE_INFO,  // id：Int类型
                BasicTypeInfo.INT_TYPE_INFO))  // age：Int类型
            .finish());

        // ToDo 2.transformation
        DataSet<Student> dataMap = dataInput.map(new MapFunction<Row, Student>() {
            @Override
            public Student map(Row row) throws Exception {  // 转换为Student类型
                return new Student(
                    (String) row.getField(0),
                    (int) row.getField(1));
            }
        });

        // ToDo 3.sink
        dataMap.print();

        // ToDo 4.execute
        env.execute();
    }

    @Data  // 注解在类上，为类提供读写属性，还提供equals()、hashCode()、toString()方法
    @AllArgsConstructor  // 注解在类上，为类提供全参构造函数，
    @NoArgsConstructor  // 注解在类上，为类提供无参构造函数
    public static class Student {
        private String user_id;
        private Integer count;
    }
```

## 1.3 Write to MySQL

```java
 public static void main(String[] args) throws Exception {

        // ToDo 0.env
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // ToDo 1.source
        DataStreamSource<Student> dataInput = env.fromCollection(
            Arrays.asList(
                new Student("31211",  20),
                new Student("331211", 19),
                new Student("3331211", 20),
                new Student("33331211",  18)
            )
        );

        // ToDo 2.transformation

        // ToDo 3.sink
        dataInput.addSink(new MySQLSink());

        // ToDo 4.execute
        env.execute();
        System.out.println("MySQL写入成功！");
    }

    @Data  // 注解在类上，为类提供读写属性，还提供equals()、hashCode()、toString()方法
    @AllArgsConstructor  // 注解在类上，为类提供全参构造函数，参数的顺序与属性定义的顺序一致
    @NoArgsConstructor  // 注解在类上，为类提供无参构造函数
    public static class Student {
        private String userId;
        private Integer count;
    }

    public static class MySQLSink extends RichSinkFunction<Student> {

        private Connection conn = null;
        private PreparedStatement insertStmt = null;
        private PreparedStatement updateStmt = null;

        // 打开数据库连接，只执行一次，之后一直使用这个连接
        @Override
        public void open(Configuration parameters) throws Exception {
            super.open(parameters);
            Class.forName("com.mysql.cj.jdbc.Driver");  // 加载数据库驱动
            conn = DriverManager.getConnection(  // 获取连接
                "jdbc:mysql://localhost:3306/test?serverTimezone=GMT%2B8&useSSL=false",  						// 数据库URL
                "root",  // 用户名
                "root");  // 登录密码
            insertStmt = conn.prepareStatement(  // 获取执行语句
                "insert into user_order_count(user_id,count) values (?,?)");  // 插入数据
            updateStmt = conn.prepareStatement(  // 获取执行语句
                "update user_order_count set count=? where user_id=?");  // 更新数据
        }

        // 执行插入和更新
        @Override
        public void invoke(Student value, Context ctx) throws Exception {
            // 每条数据到来后，直接执行更新语句
            updateStmt.setString(1, value.getUserId());  // 与占位符(?)对应的参数
            updateStmt.setInt(2, value.getCount());
            updateStmt.execute();  // 执行更新语句

            // 如果更新数为0，则执行插入语句
            if (updateStmt.getUpdateCount() == 0) {
                insertStmt.setString(1, value.getUserId());
                insertStmt.setInt(2, value.getCount());
                insertStmt.execute();  // 执行插入语句
            }
        }

        // 关闭数据库连接
        @Override
        public void close() throws Exception {
            super.close();
            if(conn != null) conn.close();
            if(insertStmt != null) insertStmt.close();
            if(updateStmt != null) updateStmt.close();
        }
    }
```

