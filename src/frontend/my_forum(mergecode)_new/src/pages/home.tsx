import { Card, Text, Badge } from "@mantine/core";
import { NavLink } from "react-router-dom";
import { Paper, Title, MultiSelect, Select } from "@mantine/core";
import { Tabs } from "@mantine/core";
import { useState, useEffect } from "react";
import { requestGetAllTags } from "../services/tag/get-all-tags";
import { requestGetAllCategories } from "../services/forum/get-all-categories";
import { requestGetAllThreads } from "../services/forum/get-all-thread";
import { ThreadFields } from "../services/forum/forum.client";
import { Autocomplete } from "@mantine/core";
import { Pagination } from "@mantine/core";
import { requestGetThreadTags } from "../services/forum/get-thread-tags";
import { Loader } from "@mantine/core";

import { ThreadCategory } from "../components/thread-category/thread-category.tsx";

import { format } from "date-fns";

export function HomePage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [suggestedThreads, setSuggestedThreads] = useState([]);
  const [value, setValue] = useState<string>("all");
  const [tagsOptions, setTagsOptions] = useState<string[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
  const [allThreads, setAllThreads] = useState<ThreadFields[]>([]);

  const [allCategories, setAllCategories] = useState<
    { value: number; label: string }[]
  >([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(0);
  const [approvedThreads, setApprovedThreads] = useState<{
    [key: number]: boolean;
  }>({});
  const pageSize = 9;
  const [threadTags, setThreadTags] = useState<{ [key: number]: string[] }>({});
  const [filteredThreads, setFilteredThreads] = useState<ThreadFields[]>([]);
  const [sortOrder, setSortOrder] = useState("desc");

  function sortThreads(threads) {
    return threads
      .filter((thread) => approvedThreads[thread.pk])
      .sort((a, b) => {
        const dateComparison =
          new Date(a.fields.created) - new Date(b.fields.created);
        return sortOrder === "asc" ? dateComparison : -dateComparison;
      });
  }
  useEffect(() => {
    if (searchQuery.trim().length > 0) {
      // Thực hiện tìm kiếm và cập nhật dữ liệu gợi ý dựa trên searchQuery
      requestGetAllThreads()
        .then((threadsResponse) => {
          const matchingThreads = threadsResponse.results.filter((thread) =>
            thread.fields.title
              .toLowerCase()
              .includes(searchQuery.toLowerCase())
          );
          setSuggestedThreads(matchingThreads);
        })
        .catch((error) => {
          console.error("Error fetching suggested threads:", error);
        });
    } else {
      setSuggestedThreads([]);
    }
  }, [searchQuery]);
  async function fetchThreadTags(threadId) {
    try {
      const tagsData = await requestGetThreadTags(threadId);
      return tagsData.results.map((tagData) => tagData.fields.tag_name);
    } catch (error) {
      console.error("Error fetching thread tags:", error);
      return [];
    }
  }

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
        const categoryOptions = response.results.map((category) => ({
          value: category.pk,
          label: `${category.fields.name} (có ID là ${category.pk})`,
        }));
        setAllCategories(categoryOptions);
      })
      .catch((error) => {
        console.error("Error fetching categories:", error);
      });

    if (value === "all" && selectedCategory === null) {
      requestGetAllThreads()
        .then(async (response) => {
          const totalCount = response.count;
          const threads = response.results
            .filter((threadModel) => {
              return threadModel.fields.parent === null;
            })
            .map((threadModel) => {
              const thread = threadModel;
              thread.path = `/question/${threadModel.pk}`;
              return thread;
            });

          const filtered = threads.filter((thread) => {
            if (selectedCategory && thread.category === selectedCategory) {
              if (selectedTags.length === 0) return true;
              return selectedTags.every(
                (tag) => threadTags[thread.pk]?.includes(tag)
              );
            } else if (selectedTags.length > 0) {
              return selectedTags.every(
                (tag) => threadTags[thread.pk]?.includes(tag)
              );
            }
            return true;
          });

          setFilteredThreads(filtered);
          setTotalPages(Math.ceil(filtered.length / pageSize));
          setAllThreads(threads);
          setTotalPages(Math.ceil(totalCount / pageSize));

          Promise.all(threads.map((thread) => fetchThreadTags(thread.pk)))
            .then((tagsArray) => {
              const threadTagsMap = {};
              tagsArray.forEach((tags, index) => {
                threadTagsMap[threads[index].pk] = tags;
              });
              setThreadTags(threadTagsMap);
            })
            .catch((error) => {
              console.error("Error fetching thread tags:", error);
            });
        })
        .catch((error) => {
          console.error("Error fetching threads:", error);
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
  const handleFilterButtonClick = () => {
    let filteredThreads = allThreads;

    if (selectedCategory !== null) {
      filteredThreads = filteredThreads.filter(
        (thread) => thread.fields.category === selectedCategory
      );
    }

    if (selectedTags.length > 0) {
      filteredThreads = filteredThreads.filter((thread) =>
        selectedTags.every((tag) => threadTags[thread.pk]?.includes(tag))
      );
    }
    if (searchQuery.trim() !== "") {
      const searchKeyword = searchQuery.toLowerCase();
      filteredThreads = filteredThreads.filter(
        (thread) =>
          thread.fields.title.toLowerCase().includes(searchKeyword) ||
          thread.fields.content.toLowerCase().includes(searchKeyword)
      );
    }

    setFilteredThreads(filteredThreads);
  };

  return (
    <>
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
          className="w-[90%] m-auto pb-20"
        >
          <Paper withBorder className="w-[100%] p-2 flex justify-between">
            <Select
              data={allCategories}
              placeholder="All Categories"
              clearButtonProps={{ "aria-label": "Clear selection" }}
              clearable
              size="sm"
              className="w-[35%]"
              value={selectedCategory}
              onChange={(value) => setSelectedCategory(value)}
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
            <button
              className="self-center bg-[#f44b3c] rounded-[7px] p-3 px-4 text-white font-bold hover:opacity-50 "
              onClick={handleFilterButtonClick}
            >
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
            <Tabs.List className="">
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
              <Tabs.Tab
                className="text-[18px]"
                value="most"
                onClick={() => handleTabChange("most")}
              >
                Ranking
              </Tabs.Tab>
              <div className="flex absolute right-0 mr-[200px]">
                <Autocomplete
                  limit={5}
                  value={searchQuery}
                  onChange={setSearchQuery}
                  label="Search"
                  placeholder="Start typing to see options"
                  data={suggestedThreads.map((thread) => thread.fields.title)}
                  className="ml-[20px] w-[350px] p-2 rounded-md border"
                />
                <button
                  className="ml-[20px] self-center bg-blue-500 text-white border-blue-500 rounded-[7px] p-3 px-6 px-4 text-white font-bold hover:opacity-50"
                  onClick={handleFilterButtonClick}
                >
                  Enter
                </button>
              </div>
            </Tabs.List>

            {value === "all" && (
              <Tabs.Panel value="all" pt="xs" className="">
                <div className="flex mt-5 flex-wrap w-[100%] ml-[30px] ">
                  {filteredThreads
                    .filter((thread) => thread.fields.parent === null)
                    // .sort(
                    //   (a, b) =>
                    //     new Date(a.fields.created) - new Date(b.fields.created)
                    // )
                    .slice((currentPage - 1) * pageSize, currentPage * pageSize)
                    .map((thread) => (
                      <NavLink
                        key={thread.pk}
                        to={thread.path}
                        className="mr-4"
                      >
                        <Card
                          key={thread.pk}
                          className="mt-11 mr-4 mt-6 w-[330px] h-[110px] pb-[100px]"
                          withBorder
                          radius={7}
                          shadow="sm"
                          padding="md"
                          component="a"
                          target="_blank"
                        >
                          {approvedThreads[thread.pk] ? (
                            <Text
                              className="text-[14px] font-bold mt-[-10px]"
                              color="green"
                            >
                              Đã duyệt
                            </Text>
                          ) : (
                            <Text className="text-[14px] font-bold" color="red">
                              Đợi duyệt
                            </Text>
                          )}
                          <ThreadCategory id={thread.fields.category} />

                          <div className="flex flex-wrap  ml-[-5px] mt-2">
                            {threadTags[thread.pk]?.map((tagName) => (
                              <Badge
                                radius="lg"
                                variant="dot"
                                key={tagName}
                                className="mr-1"
                              >
                                {tagName}
                              </Badge>
                            ))}
                          </div>

                          <Text weight={500} size="lg">
                            {thread.fields.title}
                          </Text>
                          <div
                            className="mt-[17px] text-gray-400"
                            dangerouslySetInnerHTML={{
                              __html: thread.fields.content,
                            }}
                          />
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
              <Tabs.Panel value="latest" pt="xs" className="">
                <div className="flex mt-12 flex-wrap w-[100%] ml-[30px] ">
                  <div className="mb-4 absolute mt-[-30px]">
                    <button
                      className={`px-4 py-3 rounded-[10px] font-bold transition-colors ${
                        sortOrder === "asc"
                          ? "bg-green-500 text-white"
                          : "bg-gray-400 opacity-40 text-gray-600 hover:bg-gray-300"
                      }`}
                      onClick={() => setSortOrder("asc")}
                    >
                      Sort Ascending
                    </button>
                    <button
                      className={`px-4 py-3 rounded-[10px] font-bold transition-colors ml-[20px] ${
                        sortOrder === "desc"
                          ? "bg-green-500 text-white"
                          : "bg-gray-400 opacity-40 text-gray-600 hover:bg-gray-300"
                      }`}
                      onClick={() => setSortOrder("desc")}
                    >
                      Sort Descending
                    </button>
                  </div>
                  {sortThreads(filteredThreads)
                    .slice((currentPage - 1) * pageSize, currentPage * pageSize)
                    .filter((thread) => approvedThreads[thread.pk])
                    .map((thread) => (
                      <NavLink
                        key={thread.pk}
                        to={thread.path}
                        className="mr-4"
                      >
                        <Card
                          key={thread.pk}
                          className="mr-4 mt-6 w-[330px] h-[150px]"
                          withBorder
                          radius={7}
                          shadow="sm"
                          padding="md"
                          component="a"
                          target="_blank"
                        >
                          {approvedThreads[thread.pk] ? (
                            <Text
                              className="text-[14px] font-bold mt-[-10px]"
                              color="green"
                            >
                              Đã duyệt
                            </Text>
                          ) : (
                            <Text className="text-[14px] font-bold" color="red">
                              Đợi duyệt
                            </Text>
                          )}

                          <ThreadCategory id={thread.fields.category} />
                          <div className="flex flex-wrap  ml-[-5px] mt-2">
                            {threadTags[thread.pk]?.map((tagName) => (
                              <Badge
                                radius="lg"
                                variant="dot"
                                key={tagName}
                                className="mr-1"
                              >
                                {tagName}
                              </Badge>
                            ))}
                          </div>
                          <Text weight={400} size="md">
                            {format(
                              new Date(thread.fields.created),
                              "MMMM dd, yyyy"
                            )}
                          </Text>
                          <Text weight={500} size="lg">
                            Title: {thread.fields.title}
                          </Text>

                          <div
                            className="mt-[17px] text-gray-400 "
                            dangerouslySetInnerHTML={{
                              __html: thread.fields.content,
                            }}
                          />
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
            {value === "most" && (
              <div className="mt-[90px] flex flex-col items-center">
                <Loader size="xl" variant="bars" />
                <Text className="text-[23px]">
                  Tính năng đang phát triển trong tương lai .....
                </Text>
              </div>
            )}
          </Tabs>
        </Paper>
      </div>
    </>
  );
}
