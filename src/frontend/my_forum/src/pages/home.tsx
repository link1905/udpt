import { Box, List, Card, Image, Text } from "@mantine/core";
import { NavLink } from "react-router-dom";
import { Paper, Title, MultiSelect } from "@mantine/core";
import { Tabs } from "@mantine/core";
import { useState, useEffect } from "react";
export function HomePage() {
  const [value, setValue] = useState<string>("all");
  return (
    <>
      {/* <Box>
        <List>
          <List.Item>
            <NavLink to="/question">Question list</NavLink>
          </List.Item>
          <List.Item> */}
      <NavLink to="/question/id">Question detail</NavLink>
      <br></br>
      <NavLink to="/signin">SIGN IN</NavLink>
      {/* </List.Item>
          <List.Item>
            <NavLink to="/question/create">Create question</NavLink>
          </List.Item>
        </List>
      </Box> */}

      <div className="mt-[20px] ">
        <Title color="blue.5" className="text-center mb-6 text-[50px]">
          Distributed Application Community
        </Title>
        <Title order={1} color="blue.5" className="text-center mb-6">
          The Forum
        </Title>
        <Paper
          shadow="xl"
          radius="md"
          p="lg"
          withBorder
          className="w-[90%] m-auto h-[100vh] "
        >
          <Paper withBorder className="w-[100%] p-2 flex justify-between">
            <MultiSelect
              data={[
                "React",
                "Angular",
                "Svelte",
                "Vue",
                "Riot",
                "Next.js",
                "Blitz.js",
              ]}
              placeholder="All Categories"
              defaultValue={["react", "next"]}
              clearButtonProps={{ "aria-label": "Clear selection" }}
              clearable
              size="sm"
              className="w-[35%]"
            />
            <MultiSelect
              data={[
                "Cloud",
                "Driver",
                "Import",
                "Spring",
                "Browser",
                "Operations",
                "Performance",
              ]}
              placeholder="All Tags"
              defaultValue={["react", "next"]}
              clearButtonProps={{ "aria-label": "Clear selection" }}
              clearable
              size="sm"
              className="ml-[-10px] w-[35%]"
            />
            <button className="self-center bg-[#f44b3c] rounded-[7px] p-3 px-4 text-white font-bold hover:opacity-50">
              Enter
            </button>
            <NavLink
              className=" bg-[#7A9D54] rounded-[7px] p-2 px-4 text-white font-bold hover:opacity-50"
              to="/question/create"
            >
              Create question
            </NavLink>
          </Paper>
          <Tabs className="mt-4" defaultValue="gallery">
            <Tabs.List>
              <Tabs.Tab className="text-[18px] pl-0" value="latest">
                Latest questions
              </Tabs.Tab>
              <Tabs.Tab className="text-[18px]" value="all">
                All questions
              </Tabs.Tab>
              <Tabs.Tab className="text-[18px]" value="most">
                Most viewed
              </Tabs.Tab>
            </Tabs.List>

            <Tabs.Panel value="latest" pt="xs">
              Latest questions
            </Tabs.Panel>

            {value === "all" && (
              <Tabs.Panel value="all" pt="xs" className="">
                <div className="flex mt-5">
                  <Card
                    className="mr-4"
                    withBorder
                    radius={7}
                    shadow="sm"
                    padding="md"
                    component="a"
                    target="_blank"
                  >
                    <Text weight={500} size="lg" mt="md">
                      I can't install NodeJs !!. Please help me.
                    </Text>

                    <Text mt="xs" color="dimmed" size="sm">
                      I have lot's of nodes of the same type, that have a
                      propery "genres" as a List of Strings. I want to select
                      one of these nodes and compare them to all other nodes in
                      the database only according to this one property. Nodes
                      with a huge intersection between the lists should come on
                      top
                    </Text>
                  </Card>

                  <Card
                    withBorder
                    radius={7}
                    shadow="sm"
                    padding="md"
                    component="a"
                    target="_blank"
                  >
                    <Text weight={500} size="lg" mt="md">
                      I can't install NodeJs !!. Please help me.
                    </Text>

                    <Text mt="xs" color="dimmed" size="sm">
                      I have lot's of nodes of the same type, that have a
                      propery "genres" as a List of Strings. I want to select
                      one of these nodes and compare them to all other nodes in
                      the database only according to this one property. Nodes
                      with a huge intersection between the lists should come on
                      top
                    </Text>
                  </Card>
                </div>
              </Tabs.Panel>
            )}

            <Tabs.Panel value="most" pt="xs">
              Most viewed
            </Tabs.Panel>
          </Tabs>
        </Paper>
      </div>
    </>
  );
}
