import { Card, Text } from "@mantine/core";
import { NavLink } from "react-router-dom";
import { Paper, Title, MultiSelect, Select } from "@mantine/core";
import { Tabs } from "@mantine/core";
import { useState, useEffect } from "react";
import { requestGetAllTags } from "../services/tag/get-all-tags";
import { requestGetAllCategories } from "../services/forum/get-all-tags";
import { requestGetAllThreads } from "../services/forum/get-all-thread";
import { ThreadFields } from "../services/forum/forum.client";
import { requestGetLatestThreads } from "../services/forum/get-all-thread";
import { Pagination } from "@mantine/core";
export function HomePage() {
  const [value, setValue] = useState<string>("all");
  const [tagsOptions, setTagsOptions] = useState<string[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [allThreads, setAllThreads] = useState<ThreadFields[]>([]);
  const [latestThreads, setLatestThreads] = useState<ThreadFields[]>([]);
  const [allCategories, setAllCategories] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(0);
  const [approvedThreads, setApprovedThreads] = useState<{
    [key: number]: boolean;
  }>({});
  const pageSize = 3;

  useEffect(() => {
    requestGetAllTags()
      .then((tags) => {
        const tagNames = tags.results.map((tag) => tag.fields.name);
        setTagsOptions(tagNames);
      })
      .catch((error) => {
        console.error("Error fetching tags:", error);
      });

    requestGetAllCategories()
      .then((response) => {
        const categoryOptions = response.results.map(
          (category) => category.fields.name
        );
        setAllCategories(categoryOptions);
      })
      .catch((error) => {
        console.error("Error fetching categories:", error);
      });

    if (value === "all") {
      requestGetAllThreads()
        .then((response) => {
          const totalCount = response.count;
          const threads = response.results.map((threadModel) => {
            const thread = threadModel; // Sửa đổi ở đây
            thread.path = `/question/${threadModel.pk}`;
            return thread;
          });

          setAllThreads(threads);
          setTotalPages(Math.ceil(totalCount / pageSize));
        })
        .catch((error) => {
          console.error("Error fetching threads:", error);
        });
    }
    if (value === "latest") {
      requestGetLatestThreads()
        .then((response) => {
          const threads = response.results.map((threadModel) => {
            const thread = threadModel.fields;
            thread.path = `/question/${threadModel.pk}`;
            return thread;
          });
          setLatestThreads(threads);
        })
        .catch((error) => {
          console.error("Error fetching latest threads:", error);
        });
    }
  }, [value]);

  useEffect(() => {
    const storedApprovedThreadsString = localStorage.getItem("approvedThreads");
    const storedApprovedThreads =
      storedApprovedThreadsString !== null
        ? JSON.parse(storedApprovedThreadsString)
        : {};
    setApprovedThreads(storedApprovedThreads);
  }, []);

  const handleTabChange = (newValue: string) => {
    setValue(newValue);
  };
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
            <Select
              data={allCategories}
              placeholder="All Categories"
              clearButtonProps={{ "aria-label": "Clear selection" }}
              clearable
              size="sm"
              className="w-[35%]"
            />
            <MultiSelect
              data={tagsOptions}
              placeholder="All Tags"
              value={selectedTags}
              onChange={setSelectedTags}
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
          <Tabs className="mt-4" defaultValue="all" variant="pills">
            <Tabs.List>
              <Tabs.Tab
                className="text-[18px] pl-0 pl-2"
                value="latest"
                onClick={() => handleTabChange("latest")}
              >
                Latest questions
              </Tabs.Tab>
              <Tabs.Tab
                className="text-[18px]"
                value="all"
                onClick={() => handleTabChange("all")}
              >
                All questions
              </Tabs.Tab>
              <Tabs.Tab className="text-[18px]" value="most">
                Most viewed
              </Tabs.Tab>
            </Tabs.List>

            {value === "all" && (
              <Tabs.Panel value="all" pt="xs" className="">
                <div className="flex mt-5 flex-wrap w-[100%] ml-[30px] ">
                  {allThreads
                    .slice((currentPage - 1) * pageSize, currentPage * pageSize)
                    .map((thread) => (
                      <NavLink
                        key={thread.pk}
                        to={thread.path}
                        className="mr-4"
                      >
                        <Card
                          key={thread.pk}
                          className="mr-4 mt-6 w-[330px] h-[110px]"
                          withBorder
                          radius={7}
                          shadow="sm"
                          padding="md"
                          component="a"
                          target="_blank"
                        >
                          <Text weight={500} size="lg">
                            {thread.fields.title}
                          </Text>
                          <div
                            className="mt-[2px] text-gray-400"
                            dangerouslySetInnerHTML={{
                              __html: thread.fields.content,
                            }}
                          />

                          {approvedThreads[thread.pk] ? (
                            <Text
                              className="text-[14px] font-bold"
                              color="green"
                            >
                              Đã duyệt
                            </Text>
                          ) : (
                            <Text className="text-[14px] font-bold" color="red">
                              Đợi duyệt
                            </Text>
                          )}
                        </Card>
                      </NavLink>
                    ))}
                </div>
                <Pagination
                  className="mt-[20px]"
                  total={totalPages}
                  value={currentPage}
                  onChange={setCurrentPage}
                  position="center"
                  styles={(theme) => ({
                    control: {
                      "&[data-active]": {
                        backgroundImage: theme.fn.gradient({
                          from: "red",
                          to: "yellow",
                        }),
                        border: 0,
                      },
                    },
                  })}
                />
              </Tabs.Panel>
            )}

            {value === "latest" && (
              <Tabs.Panel value="latest" pt="xs">
                <div className="flex mt-5">
                  {latestThreads.map((thread) => (
                    <NavLink key={thread.pk} to={thread.path} className="mr-4">
                      <Card
                        key={thread.pk}
                        className="mr-4"
                        withBorder
                        radius={7}
                        shadow="sm"
                        padding="md"
                        component="a"
                        target="_blank"
                      >
                        <Text weight={500} size="lg">
                          {thread.title}
                        </Text>
                        <div
                          className="mt-[10px] text-gray-400"
                          dangerouslySetInnerHTML={{ __html: thread.content }}
                        />
                      </Card>
                    </NavLink>
                  ))}
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
