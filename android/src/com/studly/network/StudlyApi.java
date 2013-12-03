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
    @POST("/add-email")
    String joinGroup(@Field("title") String title,
                     @Field("emailAddress") String email,
                     @Field("calendarId") String calendarId);
}
