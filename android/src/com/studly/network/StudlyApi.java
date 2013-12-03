package com.studly.network;

import retrofit.http.Field;
import retrofit.http.FormUrlEncoded;
import retrofit.http.GET;
import retrofit.http.POST;

import com.studly.model.StudlyMapping;

public interface StudlyApi {

    @GET("/get-mappings.json")
    StudlyMapping.List getMappings();

    @FormUrlEncoded
    @POST("/join-event")
    StudlyMapping joinGroup(@Field("title") String title,
                            @Field("calendarId") String calendarId,
                            @Field("emailAddress") String email);
}
