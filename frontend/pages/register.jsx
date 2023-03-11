import React, { useState } from "react";
import { Button, Checkbox, Form, Input } from "antd";
import { Radio } from "antd";
import { useRouter } from "next/router";
import Head from "next/head";

const App = () => {
    const router = useRouter();
    console.log(router.route);
    const [gender, setgender] = useState(true);
    const onFinish = values => {
        console.log("Success:", values);
    };

    const onFinishFailed = errorInfo => {
        console.log("Failed:", errorInfo);
    };

    return (
        <>
            <Head>
                <title>Finmanager</title>
            </Head>
            <main className="bg-transparent h-min-72">
                <Form
                    className="m-auto mt-4 p-4 pt-8 rounded-xl dark:bg-gray-400 bg-gray-300"
                    name="basic"
                    labelCol={{ span: 8 }}
                    wrapperCol={{ span: 16 }}
                    style={{ maxWidth: 400 }}
                    initialValues={{ remember: true }}
                    onFinish={onFinish}
                    onFinishFailed={onFinishFailed}
                    autoComplete="off">
                    <Form.Item
                        className="dark:text-white"
                        label="Name"
                        name="name"
                        style={{ color: "white" }}
                        rules={[
                            { required: true, message: "Enter your name!" },
                        ]}>
                        <Input type="text" placeholder="Your name" />
                    </Form.Item>
                    <Form.Item
                        className="dark:text-white"
                        label="Email"
                        name="email"
                        style={{ color: "white" }}
                        rules={[
                            {
                                required: true,
                                message: "Please input your email!",
                            },
                        ]}>
                        <Input type="email" placeholder="email" />
                    </Form.Item>

                    <Form.Item
                        label="Password"
                        name="password"
                        rules={[
                            {
                                required: true,
                                message: "Please input your password!",
                            },
                        ]}>
                        <Input.Password placeholder="password" />
                    </Form.Item>

                    <Radio.Group
                        className="ml-24"
                        onChange={e => setgender(e.target.value)}
                        value={gender}>
                        <Radio value={true}>Male</Radio>
                        <Radio value={false}>Female</Radio>
                    </Radio.Group>
                    <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                        <Button
                            type="primary"
                            className="bg-gray-700 dark:bg-slate-900 mt-4 rounded-lg"
                            htmlType="submit">
                            Register
                        </Button>
                    </Form.Item>
                </Form>
            </main>
        </>
    );
};

export default App;
